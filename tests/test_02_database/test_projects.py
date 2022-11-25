import app.database.projects as projects_engine


def test_create_project() -> None:

    projects_engine.add_project(name="Example Project")


def test_get_projects() -> None:

    projects = projects_engine.get_projects(only_active=False)

    project_names = [x.name for x in projects]

    assert "Example Project" in project_names


def test_deactivate_project() -> None:

    projects_engine.deactivate_project(id=1)

    project = projects_engine.get_project(id=1)

    assert project.active == 0


def test_get_project_activate_project() -> None:

    projects_engine.activate_project(id=1)

    project = projects_engine.get_project(id=1)

    assert project.active == 1


def test_patch_project() -> None:

    projects_engine.patch_project(id=1, name="Example Project is Real Now", active=True)

    project = projects_engine.get_project(id=1)

    assert project.active == 1


def test_delete_project() -> None:

    projects_engine.delete_project(id=1)

    project = projects_engine.get_project(id=1)

    assert project.active == 0
