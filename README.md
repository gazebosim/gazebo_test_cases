# Gazebo Jetty Tutorial Party

Welcome! The purpose of this repository is to guide the testing of various functionalities of Gazebo Jetty prior to official release.
In other words, welcome to the Tutorial Party!

## Who can contribute?

Everyone, all contributions are welcome!

### Don't have a compatible platform?

Jetty on Ubuntu is only supported on the Noble version of Ubuntu (24.04). If you don't have this platform,
there are [docker images](https://github.com/gazebosim/gz-jetty/pkgs/container/gz-jetty) ready to use.

We recommend installing
[`rocker`](https://github.com/osrf/rocker?tab=readme-ov-file#installation) for
running the docker image since it handles X11 and GPU configurations for you.
Once installed, you can run

```bash
rocker  --x11 --  ghcr.io/gazebosim/gz-jetty:main
```

to start `bash` inside a `gz-jetty` container. Then you can run any of the
Gazebo commands in the tutorial e.g., `gz sim -v4 shapes.sdf`. Alternatively,
you can run Gazebo directly through a `rocker` one-liner.

```bash
rocker  --x11 --  ghcr.io/gazebosim/gz-jetty:main gz sim -v4 shapes.sdf
```

> [!TIP]
> If you have an NVIDIA graphics card, you'll need to add `--nvidia` to the `rocker` command. See `rocker` [README](https://github.com/osrf/rocker?tab=readme-ov-file#ros-2-rviz).

> [!TIP]
> If you have an Intel integrated graphics card, you'll need to add `--devices /dev/dri` to the `rocker` command.
> See `rocker` [README](https://github.com/osrf/rocker?tab=readme-ov-file#installation).

## How to contribute?

The [Issues](https://github.com/gazebosim/gazebo_test_cases/issues) page has several tickets each containing specific instructions to test a particular functionality of Gazebo Jetty.
Each ticket will have the following sections:

1. **Setup**: Details on the desired hardware and software setup for this test. The following combinations are possible.
   1. BuildType:
      - `binary`: pre-built Debian packages from the apt repository
      - `source`: building your own workspace from source
   2. Os: `Ubuntu Noble`, `Windows` and `MacOS`
2. **Links**: Any relevant references for this test.
3. **Checks**: A list of functionalities to validate.

To contribute, first ensure if you have the relevant setup as described in the ticket.
If you don't have the setup, you can find the installation instructions at <https://gazebosim.org/docs/jetty/install>.
Next, comment on the ticket indicating your interest so that others will know
you are working on it.
Then follow the instructions to perform the necessary checks.

**All checks passed?**
Great! Attaching your terminal output (codeblock comment or gist file) or a screenshot as a form of verification is greatly appreciated.
At the end of your comment, add a specially formatted text, `[status: passed]` to let us know that it passed.

**Encountered failures?**
If one or more checks fail, please provide the error message in a codeblock comment or as a gist file attachment.
At the end of your comment, add a specially formatted text, `[status: failed]` to let us know that it failed.

## Windows Tests

Binaries for the prereleases are not available for Windows, therefore, it is necessary to build
all Gazebo packages from source following the [Install from source](https://gazebosim.org/docs/jetty/install_windows_src/) instructions.

## MacOS Tests

With the introduction of standalone executables, you should now be to run `gz
sim` without starting the server and the GUI separately.

## What if I want to test something else?

If you would like to test the functionality of any other package or extend the capabilities tested above, please reach out to us on [Discord](bit.ly/GazeboDiscord) in the in the  `#gazebo-help` channel.

## Questions

Questions related to testing may be posted on [Discord](bit.ly/GazeboDiscord) in the in the  `#gazebo-help` channel. Kindly ensure to link the relevant issue ticket when starting a new discussion.

### Tickets filtered by Setup

- [`buildType: Binary`, `os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Binary%22+label:%22os:+Ubuntu+Noble%22)
- [`buildType: Binary`, `os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Binary%22+label:%22os:+MacOS%22)
- [`buildType: Source`, `os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+Ubuntu+Noble%22)
- [`buildType: Source`, `os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+MacOS%22)
- [`buildType: Source`, `os: Windows`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+Windows%22)
- [`os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Ubuntu+Noble%22)
- [`os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+MacOS%22)
- [`os: Windows`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Windows%22)
- [`os: Any`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Any%22)

#### Zeromq and Zenoh

- [`os: Ubuntu Noble`, `transport: zeromq`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Ubuntu+Noble%22+label:%22transport:+zeromq%22)
- [`os: MacOS`, `transport: zeromq`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+MacOS%22+label:%22transport:+zeromq%22)
- [`os: Windows`, `transport: zeromq`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Windows%22+label:%22transport:+zeromq%22)

- [`os: Ubuntu Noble`, `transport: zenoh`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Ubuntu+Noble%22+label:%22transport:+zenoh%22)
- [`os: MacOS`, `transport: zenoh`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+MacOS%22+label:%22transport:+zenoh%22)
- [`os: Windows`, `transport: zenoh`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Windows%22+label:%22transport:+zenoh%22)

---

Here are some things to know about Github search:

- You can filter available results with a label by typing `label:my-label`. And it works for multiple labels: `label:my-label-1 label:my-label-2`.
- If your label has a space in it, you can put the label in quotes: `label:"my label"`.
- To show results that **don't** have a label, use a minus sign: `-label:no-results-with-this-label`.
