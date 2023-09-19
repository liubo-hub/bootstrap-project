import taichi as ti
import json
import particle_system
import numpy as np
import os

ti.init(arch=ti.gpu)

with open('./data/scenes/dragon_bath.json', 'r') as f:
    simulation_config = json.load(f)

config = simulation_config['Configuration']

box_x, box_y, box_z = config['domainEnd']

box_vertex_point = ti.Vector.field(3, dtype=ti.f32, shape=8)
box_vertex_point[0] = [0., 0., 0.]
box_vertex_point[1] = [0., box_y, 0.]
box_vertex_point[2] = [box_x, 0., 0.]
box_vertex_point[3] = [box_x, box_y, 0.]

box_vertex_point[4] = [0., 0., box_z]
box_vertex_point[5] = [0., box_y, box_z]
box_vertex_point[6] = [box_x, 0., box_z]
box_vertex_point[7] = [box_x, box_y, box_z]

box_edge_index = ti.field(dtype=ti.i32, shape=24)
for i, idx in enumerate([0, 1, 0, 2, 1, 3, 2, 3, 4, 5, 4, 6, 5, 7, 6, 7, 0, 4, 1, 5, 2, 6, 3, 7]):
    box_edge_index[i] = idx

ps = particle_system.ParticleSystem(simulation_config)
ps.memory_allocation_and_initialization_only_position()
substep = config['numberOfStepsPerRenderUpdate']

draw_object_in_mesh = False

start_step = True
ps.memory_allocation_and_initialization()
solver = ps.build_solver()
solver.initialize()
current_fluid_domain_start = [np.array(fluid['start']) for fluid in ps.fluidBlocksConfig]
current_fluid_domain_end = [np.array(fluid['end']) for fluid in ps.fluidBlocksConfig]
fluid_box_num = len(current_fluid_domain_start)

safe_boundary_start = ps.domain_start + np.array([ps.padding + ps.particle_radius])
safe_boundary_end = ps.domain_end - np.array([ps.padding + ps.particle_radius])
reallocate_memory_flag = False

include_rigid_object = True
pre_include_rigid_object = True

scene_name = 'Dragon Bath'
output_frames = False
output_interval = config['outputInterval']
output_ply = True
cnt = 0
cnt_ply = 0
series_prefix = "{}_output/particle_object_{}.ply".format(scene_name, "{}")
enter_second_phase_first_time = True
reset_scene_flag = False

while cnt<=10000:
    if start_step:
        for i in range(substep):
            solver.step()

    if not start_step:

        if include_rigid_object != pre_include_rigid_object:
            pre_include_rigid_object = include_rigid_object
            reallocate_memory_flag = True

        if reallocate_memory_flag:
            cur_object_id = 1
            del ps
            ps = particle_system.ParticleSystem(simulation_config)

            for idx in range(fluid_box_num):
                ps.fluidBlocksConfig[idx]['start'] = current_fluid_domain_start[idx]
                ps.fluidBlocksConfig[idx]['end'] = current_fluid_domain_end[idx]
            ps.memory_allocation_and_initialization_only_position()
            reallocate_memory_flag = False

    if start_step:
        if enter_second_phase_first_time:
            if output_frames:
                os.makedirs(f"{scene_name}_output_img", exist_ok=True)  # output image
            if output_ply:
                os.makedirs(f"{scene_name}_output", exist_ok=True)
            enter_second_phase_first_time = False

        if cnt % output_interval == 0:
            if output_ply:
                ps.update_fluid_position_info()
                np_position = ps.dump()
                writer = ti.tools.PLYWriter(num_vertices=ps.total_fluid_particle_num)
                writer.add_vertex_pos(np_position[:, 0], np_position[:, 1], np_position[:, 2])
                writer.export_frame_ascii(cnt_ply, series_prefix.format(0))
                for r_body_id in ps.rigid_object_id:
                    with open(f"{scene_name}_output/obj_{r_body_id}_{cnt_ply:06}.obj", "w") as f:
                        e = ps.object_collection[r_body_id]["mesh"].export(file_type='obj')
                        f.write(e)
                cnt_ply += 1

        cnt += 1
