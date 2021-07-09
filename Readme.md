# Inotify2NATS

Inotify2NATS is a simple Python application which forwards various Linux
file system inotify events onto a NATS server.

Unfortunately, at the moment, Linux filesystem inotify events are not
forwarded across *bind mounts*.

ComputePods make extensive use of bind mounts (on Linux) to allow users to
edit their files using editors of their choice. These file changes take
place *outside* of any of the ComputePods. This means that the MajorDomo
processes *inside* the pods in a federation of ComputePods, will never be
notified that a user's file has been altered, and hence will never
automatically restart the build process which is the primary purpose of
any federation of ComputePods.

Inotify2NATS is designed to solve this problem.
