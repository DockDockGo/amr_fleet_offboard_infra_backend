# Generated by Django 4.2.7 on 2023-12-15 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AMRMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_workflow_id', models.IntegerField(blank=True, null=True)),
                ('material_transport_task_chain_id', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'BACKLOG'), (2, 'ENQUEUED'), (3, 'RUNNING'), (4, 'COMPLETED'), (5, 'FAILED'), (6, 'CANCELED')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enqueue_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('amr_id', models.IntegerField(blank=True, choices=[(1, 'AMR_1'), (2, 'AMR_2')], null=True)),
                ('start', models.IntegerField(choices=[(0, 'UNDEFINED'), (6, 'INSPECTION'), (1, 'ROBOT_ARM_1'), (2, 'ROBOT_ARM_2'), (4, 'DEPOT'), (5, 'ROBOT_ARM_3')])),
                ('goal', models.IntegerField(choices=[(0, 'UNDEFINED'), (6, 'INSPECTION'), (1, 'ROBOT_ARM_1'), (2, 'ROBOT_ARM_2'), (4, 'DEPOT'), (5, 'ROBOT_ARM_3')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestbedTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_workflow_id', models.IntegerField(blank=True, null=True)),
                ('material_transport_task_chain_id', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'BACKLOG'), (2, 'ENQUEUED'), (3, 'RUNNING'), (4, 'COMPLETED'), (5, 'FAILED'), (6, 'CANCELED')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enqueue_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('workcell_id', models.IntegerField(choices=[(0, 'UNDEFINED'), (6, 'INSPECTION'), (1, 'ROBOT_ARM_1'), (2, 'ROBOT_ARM_2'), (4, 'DEPOT'), (5, 'ROBOT_ARM_3')])),
                ('testbed_task_type', models.IntegerField(blank=True, choices=[(1, 'UNLOADING'), (2, 'PROCESSING'), (3, 'LOADING')], null=True)),
                ('assembly_type_id', models.IntegerField(blank=True, choices=[(1, 'M'), (2, 'F'), (3, 'I')], null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkCellState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workcell_id', models.IntegerField(choices=[(0, 'UNDEFINED'), (6, 'INSPECTION'), (1, 'ROBOT_ARM_1'), (2, 'ROBOT_ARM_2'), (4, 'DEPOT'), (5, 'ROBOT_ARM_3')])),
                ('docked_amr_id', models.IntegerField(blank=True, choices=[(1, 'AMR_1'), (2, 'AMR_2')], null=True)),
                ('active_task', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testbed_emulator_backend_app.testbedtask')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialTransportTaskChain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_workflow_id', models.IntegerField()),
                ('loading_subtask', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='loading_subtask_material_transport_task_chain', to='testbed_emulator_backend_app.testbedtask')),
                ('navigate_to_sink_subtask', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testbed_emulator_backend_app.amrmission')),
                ('navigate_to_source_subtask', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='navigate_to_source_subtask_material_transport_task_chain', to='testbed_emulator_backend_app.amrmission')),
                ('unloading_subtask', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unloading_subtask_material_transport_task_chain', to='testbed_emulator_backend_app.testbedtask')),
            ],
        ),
        migrations.CreateModel(
            name='AssemblyWorkflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_assembly_type_id', models.IntegerField()),
                ('assembly_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='assembly_task_assembly_workflow', to='testbed_emulator_backend_app.testbedtask')),
                ('fetch_parts_bins', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fetch_parts_bins_assembly_workflow', to='testbed_emulator_backend_app.testbedtask')),
                ('kitting_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='kitting_task_assembly_workflow', to='testbed_emulator_backend_app.testbedtask')),
                ('transport_assembly_task_payload_to_qa_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transport_assembly_task_payload_to_qa_station_assembly_workflow', to='testbed_emulator_backend_app.materialtransporttaskchain')),
                ('transport_kitting_task_payload_to_assembly_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transport_kitting_task_payload_to_assembly_station_assembly_workflow', to='testbed_emulator_backend_app.materialtransporttaskchain')),
                ('transport_parts_bins_to_kitting_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transport_parts_bins_to_kitting_station_assembly_workflow', to='testbed_emulator_backend_app.materialtransporttaskchain')),
            ],
        ),
        migrations.CreateModel(
            name='AMRState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amr_id', models.IntegerField(blank=True, choices=[(1, 'AMR_1'), (2, 'AMR_2')], null=True, unique=True)),
                ('active_material_transport_task_chain', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testbed_emulator_backend_app.materialtransporttaskchain')),
                ('active_mission', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testbed_emulator_backend_app.amrmission')),
            ],
        ),
    ]
