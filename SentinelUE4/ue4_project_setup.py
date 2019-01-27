import git
import logging
logging.basicConfig(level=logging.INFO)

path = "D:/Work/BusMoneyGames/UE4/"


def clone_project_engine(unreal_project_info):
    engine_path = unreal_project_info.settings.get_default_engine_path()
    print(engine_path)

    repo = git.Repo.clone_from("git@github.com:BusMoneyGames/UnrealEngine.git", engine_path)
