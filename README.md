# Gazebo Harmonic Tutorial Party
Welcome! The purpose of this repository is to guide the testing of various functionalities of Gazebo Harmonic prior to official release.
In other words, welcome to the Tutorial Party!

## Who can contribute?
Everyone, all contributions are welcome!

## How to contribute?
The [Issues](https://github.com/gazebosim/gazebo_test_cases/issues) page has several tickets each containing specific instructions to test a particular functionality of Gazebo Harmonic.
Each ticket will have the following sections:

1. **Setup**: Details on the desired hardware and software setup for this test. The following combinations are possible.
   1. BuildType: 
      * `binary`: pre-built debian packages from the apt repository
      * `source`: building your own workspace from source
   2. Os: `Ubuntu Jammy`, `Windows` and `MacOS`
2. **Links**: Any relevant references for this test.
3. **Checks**: A list of functionalities to validate.

To contribute, first ensure if you have the relevant setup as described in the ticket.
If you don't have the setup, you can find the installation instructions at https://gazebosim.org/docs/harmonic/install.
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
Questions related to testing may be posted as a new [Issue](https://github.com/gazebosim/gazebo_test_cases/issues). Kindly ensure to link the relevant issue ticket when starting a new discussion.

## Timeline
We are expecting to generate all the issues for this tutorial party in two batches to ensure that we validate the test cases with a higher priority. The batches will release in the following order:
- First Batch: August 31st
    - All the test cases related with Ubuntu
    - Only the test cases from the docs for MacOS and Windows.
- Second Batch: September 11th
    - The rest of the test cases for MacOS and Windows. 

---

### Tickets filtered by Setup

- [ ] [Ubuntu Jammy, Binary](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22)

  <details><summary>Labels</summary>

  - [ ] [docs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22docs%22)
  - [ ] [harmonic](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22harmonic%22)
  - [ ] [gz-common](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-common%22)
  - [ ] [gz-fuel-tools](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-fuel-tools%22)
  - [ ] [gz-gui](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-gui%22)
  - [ ] [gz-launch](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-launch%22)
  - [ ] [gz-math](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-math%22)
  - [ ] [gz-msgs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-msgs%22)
  - [ ] [gz-physics](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-physics%22)
  - [ ] [gz-plugin](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-plugin%22)
  - [ ] [gz-rendering](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-rendering%22)
  - [ ] [gz-sensors](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-sensors%22)
  - [ ] [gz-sim](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-sim%22)
  - [ ] [gz-tools](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-tools%22)
  - [ ] [gz-transport](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-transport%22)
  - [ ] [gz-utils](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22gz-utils%22)
  - [ ] [sdf_tutorials](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22sdf_tutorials%22)
  - [ ] [sdformat](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22sdformat%22)
  - [ ] [sdf worlds](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Binary%22+label:%22generation-1%22+label:%22sdf%20worlds%22)

  </details>
- [ ] [Ubuntu Jammy, Source](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22)

  <details><summary>Labels</summary>

  - [ ] [docs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22docs%22)
  - [ ] [harmonic](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22harmonic%22)
  - [ ] [gz-common](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-common%22)
  - [ ] [gz-fuel-tools](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-fuel-tools%22)
  - [ ] [gz-gui](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-gui%22)
  - [ ] [gz-launch](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-launch%22)
  - [ ] [gz-math](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-math%22)
  - [ ] [gz-msgs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-msgs%22)
  - [ ] [gz-physics](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-physics%22)
  - [ ] [gz-plugin](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-plugin%22)
  - [ ] [gz-rendering](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-rendering%22)
  - [ ] [gz-sensors](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-sensors%22)
  - [ ] [gz-sim](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-sim%22)
  - [ ] [gz-tools](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-tools%22)
  - [ ] [gz-transport](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-transport%22)
  - [ ] [gz-utils](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22gz-utils%22)
  - [ ] [sdf_tutorials](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22sdf_tutorials%22)
  - [ ] [sdformat](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Ubuntu%20Jammy%22+label:%22Source%22+label:%22generation-1%22+label:%22sdformat%22)

  </details>
- [ ] [MacOS, Source](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Source%22+label:%22generation-1%22)

  <details><summary>Labels</summary>

  - [ ] [docs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Source%22+label:%22generation-1%22+label:%22docs%22)
  - [ ] [harmonic](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Source%22+label:%22generation-1%22+label:%22harmonic%22)

  </details>
- [ ] [MacOS, Binary](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Binary%22+label:%22generation-1%22)

  <details><summary>Labels</summary>

  - [ ] [docs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Binary%22+label:%22generation-1%22+label:%22docs%22)
  - [ ] [harmonic](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22MacOS%22+label:%22Binary%22+label:%22generation-1%22+label:%22harmonic%22)

  </details>
- [ ] [Windows, Binary](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Windows%22+label:%22Binary%22+label:%22generation-1%22)

  <details><summary>Labels</summary>

  - [ ] [docs](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Windows%22+label:%22Binary%22+label:%22generation-1%22+label:%22docs%22)
  - [ ] [harmonic](https://github.com/Voldivh/gazebo_test_cases/issues?q=is%3Aissue+is%3Aopen+label:%22Windows%22+label:%22Binary%22+label:%22generation-1%22+label:%22harmonic%22)

  </details>
