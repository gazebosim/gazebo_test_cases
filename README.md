# Gazebo Ionic Tutorial Party

Welcome! The purpose of this repository is to guide the testing of various functionalities of Gazebo Ionic prior to official release.
In other words, welcome to the Tutorial Party!

## Who can contribute?

Everyone, all contributions are welcome!

### Don't have a compatible platform?

Ionic on Ubuntu is only supported on the Noble version of Ubuntu (24.04). If you don't have this plaform, there are [docker images
and instructions](https://github.com/j-rivero/ionic_testing) ready to use.

## How to contribute?

The [Issues](https://github.com/gazebosim/gazebo_test_cases/issues) page has several tickets each containing specific instructions to test a particular functionality of Gazebo Ionic.
Each ticket will have the following sections:

1. **Setup**: Details on the desired hardware and software setup for this test. The following combinations are possible.
   1. BuildType:
      * `binary`: pre-built debian packages from the apt repository
      * `source`: building your own workspace from source
   2. Os: `Ubuntu Noble`, `Windows` and `MacOS`
2. **Links**: Any relevant references for this test.
3. **Checks**: A list of functionalities to validate.

To contribute, first ensure if you have the relevant setup as described in the ticket.
If you don't have the setup, you can find the installation instructions at https://gazebosim.org/docs/ionic/install.
Next, assign the ticket to yourself via the `Assignees` option or comment on the ticket indicating your interest.
Then follow the instructions to perform the necessary checks.

**All checks passed?**
Great! Please tick the checkboxes if you can or else leave a comment indicating your successful testing. Attaching your terminal output (codeblock comment or gist file) as a form of verification is greatly appreciated.
If you have the necessary permission, go ahead and close the ticket by clicking `Close as completed`.

**Encountered failures?**
If one or more checks fail, please provide the error message in a codeblock comment or as a gist file attachment.

## What if I want to test something else?
If you would like to test the functionality of any other package or extend the capabilities tested above, please open additional tickets while following the format described above.

## Questions
Questions related to testing may be posted on the [Discussions](https://github.com/gazebosim/gazebo_test_cases/discussions) board. Kindly ensure to link the relevant issue ticket when starting a new discussion.

### Tickets filtered by Setup

- [`os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Ubuntu+Noble%22)
- [`buildType: Source`, `os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+Ubuntu+Noble%22)
- [`buildType: Binary`, `os: Ubuntu Noble`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Binary%22+label:%22os:+Ubuntu+Noble%22)
- [`os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+MacOS%22)
- [`buildType: Source`, `os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+MacOS%22)
- [`os: Windows`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Windows%22)
- [`buildType: Source`, `os: Windows`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Source%22+label:%22os:+Windows%22)
- [`os: Any`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22os:+Any%22)
- [`buildType: Binary`, `os: MacOS`](https://github.com/gazebosim/gazebo_test_cases/issues?q=is:issue+is:open+label:%22buildType:+Binary%22+label:%22os:+MacOS%22)

---

Here are some things to know about Github search:
- You can filter available results with a label by typing `label:my-label`. And it works for multiple labels: `label:my-label-1 label:my-label-2`.
- If your label has a space in it, you can put the label in quotes: `label:"my label"`.
- To show results that **don't** have a label, use a minus sign: `-label:no-results-with-this-label`.

