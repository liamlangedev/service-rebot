def test_package_imports():
    import rebot_trash_sorting
    from rebotarm_msgs.action import MoveToPose
    from rebotarm_msgs.srv import MoveToPoseIK, SetGripper

    assert rebot_trash_sorting is not None
    assert MoveToPose is not None
    assert MoveToPoseIK is not None
    assert SetGripper is not None
