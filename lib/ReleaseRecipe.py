import requests
import re
from os import sys
sys.path.append('./..')

artifact_url = "http://jenkins.shn.io/job/EngTools-list-articorp-releases/lastSuccessfulBuild/artifact/corp-releases.properties/*view*/"
artifact_json = 'http://jenkins.shn.io/job/EngTools-list-articorp-releases/lastSuccessfulBuild/artifact/artifacts.json/*view*/'
timeout = 10

class VpnException(Exception):
    pass


class ReleaseRecipe:
    def __init__(self):
        self.artifact_url = artifact_json
        self.all_artifacts = None

    def _get_all_artifacts(self):
        if not self.all_artifacts:
            self.refresh_artifacts()
        return self.all_artifacts

    def refresh_artifacts(self):
        try:
            resp = requests.get(self.artifact_url, timeout=timeout)
        except Exception as e:
            raise type(e)("Not able to reach VPN...\nConnect to McAfee VPN.")
        if resp.status_code != 200:
            raise VpnException("Incorrect VPN...\nConnect to McAfee VPN.")
        self.all_artifacts = resp.json()
        return self.all_artifacts

    def get_all_tp_artifacts(self, pipeline):
        all_artifacts = self._get_all_artifacts()
        set_all_artifact_keys = set(all_artifacts.keys())
        recipe_components = self._get_recipe_component_list(pipeline)
        tp_artifacts = list()
        for recipe_item in recipe_components:
            if recipe_item.replace('-', '_').upper() in set_all_artifact_keys:
                tp_artifacts.append(all_artifacts[recipe_item.replace('-', '_').upper()])
        return (tp_artifacts)

    def get_builds_with_name(self, keyword='tp-default'):
        """

        :param keyword:one of (['builds', 'default', 'latest_5.3', 'latest_5.3.0', 'latest_release', 'latest_stable',
        'latest_trunk', 'releases'])
        :return:
        """
        pipeline, build_type = keyword.split('-')
        all_builds = self.get_all_tp_artifacts(pipeline)
        result_builds = list()

        for component in all_builds:
            component_build = component.get(build_type)
            if component_build:
                result_builds.append(component_build)
            else:
                result_builds.append(component.get('default'))
        return ', '.join(result_builds)

    def _get_recipe_component_list(self, pipeline):
        if pipeline == 'tp':
            recipe_file = 'resource/tp_recipe_components.txt'
        else:
            recipe_file = 'resource/dp_recipe_components.txt'

        with open(recipe_file, 'r') as recipe:
            return [line.strip() for line in recipe]


if __name__ == "__main__":
    rr = ReleaseRecipe()
    artifacts = rr.refresh_artifacts()
    dp_list = rr._get_recipe_component_list('dp')

    for item in dp_list:
        for key in artifacts.keys():
            if key.lower().startswith(item.lower()):
                print(key.lower())
                break
        else:
            # print("not found : ", item)
            pass
