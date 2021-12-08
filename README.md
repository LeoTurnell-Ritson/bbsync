<h1 align="center">bbsync</h1>

<p align="center">
  wrapper for shh/rsync for use with OpenFOAM and blue bear
  </p>
</div>


## About The Project

bbsync is a wrapper for shh/rsync for use with [OpenFOAM](https://www.openfoam.com/) and [blue bear](https://intranet.birmingham.ac.uk/it/teams/infrastructure/research/bear/bluebear/index.aspx), application may be limited if your not using both these platforms. The fundamental idea is to be able to push and pull src, applications and folders in the OpenFOAM run directory to and from blue bear, using relative user-defined paths (see example-bashrc).

## Getting Started

### Prerequisites

* pyinstaller
  ```sh
  pip3 install pyinstaller
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/LeoTurnell-Ritson/bbsync.git
   ```
3. Run Allmake
   ```sh
   ./Allmake
   ```
4. Add bbsync to path
   ```sh
   export PATH=$PATH:$(pwd)/dist
   ```
### Running bbsync

To run bbsync, first you should make of copy of and edit the example-bahrc file to fit your blue bear environment, then source it. Additionaly you'll need to be connected to the blue bear severs. To check that the configuration is working try:

```sh
bbsync -c 'echo Hello World!'
```

For more information on the commands try:

```sh
bbsync --help
```