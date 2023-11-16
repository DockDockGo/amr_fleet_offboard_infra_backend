# Generated by Django 4.2.7 on 2023-11-16 04:19

from django.db import migrations, models
import django.db.models.deletion
import testbed_emulator_backend_app.testbed_config


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AMRMission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_workflow_id', models.IntegerField()),
                ('status', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.TaskStatus['BACKLOG'], 1), (testbed_emulator_backend_app.testbed_config.TaskStatus['ENQUEUED'], 2), (testbed_emulator_backend_app.testbed_config.TaskStatus['RUNNING'], 3), (testbed_emulator_backend_app.testbed_config.TaskStatus['COMPLETED'], 4), (testbed_emulator_backend_app.testbed_config.TaskStatus['FAILED'], 5), (testbed_emulator_backend_app.testbed_config.TaskStatus['CANCELED'], 6)], default=1, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enqueue_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('amr_id', models.CharField(blank=True, choices=[(testbed_emulator_backend_app.testbed_config.AMR['RICK'], 1), (testbed_emulator_backend_app.testbed_config.AMR['MORTY'], 2)], max_length=20, null=True)),
                ('start', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.WorkCell['STOCK_ROOM'], 1), (testbed_emulator_backend_app.testbed_config.WorkCell['KITTING_STATION'], 2), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_1'], 3), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_2'], 4), (testbed_emulator_backend_app.testbed_config.WorkCell['QA_STATION'], 5)], max_length=20)),
                ('goal', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.WorkCell['STOCK_ROOM'], 1), (testbed_emulator_backend_app.testbed_config.WorkCell['KITTING_STATION'], 2), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_1'], 3), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_2'], 4), (testbed_emulator_backend_app.testbed_config.WorkCell['QA_STATION'], 5)], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TestbedTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assembly_workflow_id', models.IntegerField()),
                ('status', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.TaskStatus['BACKLOG'], 1), (testbed_emulator_backend_app.testbed_config.TaskStatus['ENQUEUED'], 2), (testbed_emulator_backend_app.testbed_config.TaskStatus['RUNNING'], 3), (testbed_emulator_backend_app.testbed_config.TaskStatus['COMPLETED'], 4), (testbed_emulator_backend_app.testbed_config.TaskStatus['FAILED'], 5), (testbed_emulator_backend_app.testbed_config.TaskStatus['CANCELED'], 6)], default=1, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enqueue_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('workcell_id', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.WorkCell['STOCK_ROOM'], 1), (testbed_emulator_backend_app.testbed_config.WorkCell['KITTING_STATION'], 2), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_1'], 3), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_2'], 4), (testbed_emulator_backend_app.testbed_config.WorkCell['QA_STATION'], 5)], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkCellState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workcell_id', models.CharField(choices=[(testbed_emulator_backend_app.testbed_config.WorkCell['STOCK_ROOM'], 1), (testbed_emulator_backend_app.testbed_config.WorkCell['KITTING_STATION'], 2), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_1'], 3), (testbed_emulator_backend_app.testbed_config.WorkCell['ASSEMBLY_STATION_2'], 4), (testbed_emulator_backend_app.testbed_config.WorkCell['QA_STATION'], 5)], max_length=20)),
                ('docked_amr_id', models.CharField(blank=True, choices=[(testbed_emulator_backend_app.testbed_config.AMR['RICK'], 1), (testbed_emulator_backend_app.testbed_config.AMR['MORTY'], 2)], max_length=20, null=True)),
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
                ('amr_id', models.CharField(blank=True, choices=[(testbed_emulator_backend_app.testbed_config.AMR['RICK'], 1), (testbed_emulator_backend_app.testbed_config.AMR['MORTY'], 2)], max_length=20, null=True)),
                ('active_mission', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='testbed_emulator_backend_app.amrmission')),
            ],
        ),
    ]