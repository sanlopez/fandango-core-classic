import argparse
import json
import datetime
import subprocess
import configparser
import os
from db.utils import check_today_projects, create_new_project, update_project, delete_project

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.yaml'))

plugins_path = config['PLUGINS'].get('PATH')
conda_envs_path = config['CONDA'].get('ENVS_PATH')

def load_args_schema(action):
    with open('args_schema.json') as f:
        args_schema = json.load(f)
    return args_schema.get(action, [])

def main():
    parser = argparse.ArgumentParser(description='FandanGO application')
    parser.add_argument('--action', choices=['createProject', 'deleteProject', 'copyData'],
                        help='Action to perform', required=True)

    fixed_args, additional_args = parser.parse_known_args()

    # check if the user provided the required args for the chosen action
    args_schema = load_args_schema(fixed_args.action)
    for arg in args_schema:
        parser.add_argument(arg['name'], help=arg['help'], required=arg['required'])
    parser.parse_known_args()

    # format additional args
    additional_args_parsed = {arg.split('=')[0]: arg.split('=')[1] for arg in additional_args}

    # core internal actions (createProject, deleteProject, etc.)
    if fixed_args.action == 'createProject':
        print('FandanGO will create a new project...')
        today_projects = check_today_projects()
        project_id = datetime.datetime.now().strftime('%Y%m%d') + str(today_projects + 1)
        new_project = (project_id, int(datetime.datetime.now().timestamp()), None, None, None)
        create_new_project(new_project)

    elif fixed_args.action == 'deleteProject':
        print('FandanGO will delete an existing project...')
        delete_project(additional_args_parsed['--projectId'])

    # actions involving other plugins
    elif additional_args_parsed['--plugin']:
        try:
            # plugin conda environment should be named fandango_pluginName_env
            python_cmd = os.path.join(conda_envs_path, f'fandango_{additional_args_parsed["--plugin"]}_env', 'bin', 'python')
            # plugin main python file should be placed at $plugins_path/fandango-pluginName/main.py
            plugin_main_path = os.path.join(plugins_path, f'fandango-{additional_args_parsed["--plugin"]}', 'main.py')
            # args properly formatted
            args_cmd = [f'--action={fixed_args.action}'] + [f"{key}={value}" for key, value in additional_args_parsed.items()]
            print(f'Sending action to plugin {additional_args_parsed["--plugin"]}: {python_cmd} {plugin_main_path} {" ".join(args_cmd)} ...')
            process = subprocess.Popen([python_cmd] + [plugin_main_path] + args_cmd, stdout=subprocess.PIPE, text=True)
            process.wait()

            for output in process.stdout:
                print(output)
                if output.startswith('{\"success'):
                    body = json.loads(output)
                    # plugin finished the action
                    if body['success']:
                        if fixed_args.action == 'copyData':
                            update_project(additional_args_parsed['--projectId'], 'data_management_system', "'" + additional_args_parsed['--plugin'] + "'")
                        elif fixed_args.action == 'associateProject':
                            update_project(additional_args_parsed['--projectId'], 'proposal_manager', "'" + additional_args_parsed['--plugin'] + "'")

        except Exception as e:
            print(f'Error sending action to plugin {additional_args_parsed["--plugin"]}. Error: {e}')

if __name__ == '__main__':
    main()
