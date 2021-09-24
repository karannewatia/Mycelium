#!/bin/bash
curl https://sh.rustup.rs -sSf | sh
git clone https://github.com/ZoKrates/ZoKrates
cd ZoKrates/
git checkout 0.7.0
git pull origin 0.7.0
rustup default 1.54
rustup install nightly-2021-06-30
cargo +nightly-2021-06-30 build --release
cd ..
