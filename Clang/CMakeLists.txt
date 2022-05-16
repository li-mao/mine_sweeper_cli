cmake_minimum_required(VERSION 3.15)

project(mine_sweeper_cli)

set(CMAKE_CXX_STANDARD 11)

add_executable(mine_sweeper_cli main.c mineObj.c)
