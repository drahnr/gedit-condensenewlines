#!/usr/bin/env bash


GEDIT_PLUGIN_DIR="$HOME/.local/share/gedit/plugins/"
mkdir -p "$GEDIT_PLUGIN_DIR"
cp -vf ./*.plugin "$GEDIT_PLUGIN_DIR"
cp -vf ./*.py "$GEDIT_PLUGIN_DIR"
