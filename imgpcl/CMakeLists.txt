cmake_minimum_required(VERSION 2.8.3)
project(imgpcl)

## Add support for C++11, supported in ROS Kinetic and newer
# add_definitions(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  pcl_conversions
  pcl_msgs
  pcl_ros
  roscpp
  rospy
  sensor_msgs
  std_msgs
  geometry_msgs

 message_generation#msg
)
find_package(PCL REQUIRED)
## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

## To declare and build messages, services or actions from within this
## package, follow these steps:
## * Let MSG_DEP_SET be the set of packages whose message types you use in
##   your messages/services/actions (e.g. std_msgs, actionlib_msgs, ...).
## * In the file package.xml:
##   * add a build_depend tag for "message_generation"
##   * add a build_depend and a run_depend tag for each package in MSG_DEP_SET
##   * If MSG_DEP_SET isn't empty the following dependency has been pulled in
##     but can be declared for certainty nonetheless:
##     * add a run_depend tag for "message_runtime"
## * In this file (CMakeLists.txt):
##   * add "message_generation" and every package in MSG_DEP_SET to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * add "message_runtime" and every package in MSG_DEP_SET to
##     catkin_package(CATKIN_DEPENDS ...)
##   * uncomment the add_*_files sections below as needed
##     and list every .msg/.srv/.action file to be processed
##   * uncomment the generate_messages entry below
##   * add every package in MSG_DEP_SET to generate_messages(DEPENDENCIES ...)

## Generate messages in the 'msg' folder
 add_message_files(
    FILES
    pos.msg
#   Message2.msg
 )

## Generate services in the 'srv' folder
# add_service_files(
#   FILES
#   Service1.srv
#   Service2.srv
# )

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   #pcl_msgs#   
   #sensor_msgs#
   std_msgs
   geometry_msgs
 )

################################################
## Declare ROS dynamic reconfigure parameters ##
################################################

## To declare and build dynamic reconfigure parameters within this
## package, follow these steps:
## * In the file package.xml:
##   * add a build_depend and a run_depend tag for "dynamic_reconfigure"
## * In this file (CMakeLists.txt):
##   * add "dynamic_reconfigure" to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * uncomment the "generate_dynamic_reconfigure_options" section below
##     and list every .cfg file to be processed

## Generate dynamic reconfigure parameters in the 'cfg' folder
# generate_dynamic_reconfigure_options(
#   cfg/DynReconf1.cfg
#   cfg/DynReconf2.cfg
# )

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
CATKIN_DEPENDS message_runtime#msg
   INCLUDE_DIRS include# INCLUDE_DIRS: uncomment this if you package contains header files
   LIBRARIES imgpcl# LIBRARIES: libraries you create in this project that dependent projects also need
#  CATKIN_DEPENDS cv_bridge image_transport pcl_conversions pcl_msgs pcl_ros roscpp rospy sensor_msgs std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
include
  ${catkin_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
)

## Declare a C++ library
# add_library(${PROJECT_NAME}
#   src/${PROJECT_NAME}/imgpcl.cpp
# )

## Add cmake target dependencies of the library
## as an example, code may need to be generated before libraries
## either from message generation or dynamic reconfigure
# add_dependencies(${PROJECT_NAME} ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Declare a C++ executable
## With catkin_make all packages are built within a single CMake context
## The recommended prefix ensures that target names across packages don't collide
# add_executable(${PROJECT_NAME}_node src/imgpcl_node.cpp)

## Rename C++ executable without prefix
## The above recommended prefix causes long target names, the following renames the
## target back to the shorter version for ease of user use
## e.g. "rosrun someones_pkg node" instead of "rosrun someones_pkg someones_pkg_node"
# set_target_properties(${PROJECT_NAME}_node PROPERTIES OUTPUT_NAME node PREFIX "")

## Add cmake target dependencies of the executable
## same as for the library above
# add_dependencies(${PROJECT_NAME}_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

## Specify libraries to link a library or executable target against
# target_link_libraries(${PROJECT_NAME}_node
#   ${catkin_LIBRARIES}
# )

#############
## Install ##
#############

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
# install(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark executables and/or libraries for installation
# install(TARGETS ${PROJECT_NAME} ${PROJECT_NAME}_node
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark cpp header files for installation
# install(DIRECTORY include/${PROJECT_NAME}/
#   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
#   FILES_MATCHING PATTERN "*.h"
#   PATTERN ".svn" EXCLUDE
# )

## Mark other files for installation (e.g. launch and bag files, etc.)
# install(FILES
#   # myfile1
#   # myfile2
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )

#############
## Testing ##
#############
link_directories(${PCL_LIBRARY_DIRS})
#add_definitions(${PCL_DEFINITIONS})
## Add gtest based cpp test target and link libraries
# catkin_add_gtest(${PROJECT_NAME}-test test/test_imgpcl.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
add_executable(calibratePrimeArm src/calibratePrimeArm.cpp)
add_dependencies(calibratePrimeArm imgpcl_generate_messages_cpp)
target_link_libraries(calibratePrimeArm ${catkin_LIBRARIES})

add_executable(capimg src/capimg.cpp)
add_dependencies(capimg imgpcl_generate_messages_cpp)
target_link_libraries(capimg ${catkin_LIBRARIES})

add_executable(capimg_mouse src/capimg_mouse.cpp)
add_dependencies(capimg_mouse imgpcl_generate_messages_cpp)
target_link_libraries(capimg_mouse ${catkin_LIBRARIES})

add_executable(camshift src/camshift.cpp)
add_dependencies(camshift imgpcl_generate_messages_cpp)
target_link_libraries(camshift ${catkin_LIBRARIES})

add_executable(template src/template.cpp)
add_dependencies(template imgpcl_generate_messages_cpp)
target_link_libraries(template ${catkin_LIBRARIES})

add_executable(changchengobjDetect src/changchengobjDetect.cpp)
add_dependencies(changchengobjDetect imgpcl_generate_messages_cpp)
target_link_libraries(changchengobjDetect ${catkin_LIBRARIES})

add_executable(obj_gpsr2017 src/obj_gpsr2017.cpp)
add_dependencies(obj_gpsr2017 imgpcl_generate_messages_cpp)
target_link_libraries(obj_gpsr2017 ${catkin_LIBRARIES} ${PCL_LIBRARIES})

add_executable(obj2017_test src/obj2017_test.cpp)
add_dependencies(obj2017_test imgpcl_generate_messages_cpp)
target_link_libraries(obj2017_test ${catkin_LIBRARIES})

add_executable(ed_obj_restaurant src/ed_obj_restaurant.cpp)
add_dependencies(ed_obj_restaurant imgpcl_generate_messages_cpp)
target_link_libraries(ed_obj_restaurant ${catkin_LIBRARIES})

add_executable(iran_storing src/iran_storing.cpp)
add_dependencies(iran_storing imgpcl_generate_messages_cpp)
target_link_libraries(iran_storing ${catkin_LIBRARIES})

add_executable(storing2017 src/storing2017.cpp)
add_dependencies(storing2017 imgpcl_generate_messages_cpp)
target_link_libraries(storing2017 ${catkin_LIBRARIES})

add_executable(gender_train src/gender_train.cpp)
add_dependencies(gender_train imgpcl_generate_messages_cpp)
target_link_libraries(gender_train ${catkin_LIBRARIES})

add_executable(gender2016hsn src/gender2016hsn.cpp)
add_dependencies(gender2016hsn imgpcl_generate_messages_cpp)
target_link_libraries(gender2016hsn ${catkin_LIBRARIES})

add_executable(gender2017 src/gender2017.cpp)
add_dependencies(gender2017 imgpcl_generate_messages_cpp)
target_link_libraries(gender2017 ${catkin_LIBRARIES})

add_executable(find_person2017_help src/find_person2017_help.cpp)
add_dependencies(find_person2017_help imgpcl_generate_messages_cpp)
target_link_libraries(find_person2017_help ${catkin_LIBRARIES})

add_executable(find_person2017_gpsr src/find_person2017_gpsr.cpp)
add_dependencies(find_person2017_gpsr imgpcl_generate_messages_cpp)
target_link_libraries(find_person2017_gpsr ${catkin_LIBRARIES})

add_executable(wave_detect src/wave_detect.cpp)
add_dependencies(wave_detect imgpcl_generate_messages_cpp)
target_link_libraries(wave_detect ${catkin_LIBRARIES})

add_executable(findaperson_pcl2016 src/findaperson_pcl2016.cpp)
add_dependencies(findaperson_pcl2016 imgpcl_generate_messages_cpp)
target_link_libraries(findaperson_pcl2016 ${catkin_LIBRARIES})

add_executable(general_obj2016 src/general_obj2016.cpp)
add_dependencies(general_obj2016 imgpcl_generate_messages_cpp)
target_link_libraries(general_obj2016 ${catkin_LIBRARIES})

add_executable(hog_followme src/hog_followme.cpp)
add_dependencies(hog_followme imgpcl_generate_messages_cpp)
target_link_libraries(hog_followme ${catkin_LIBRARIES})

add_executable(objectdetect_test src/objectdetect_test.cpp)
add_dependencies(objectdetect_test imgpcl_generate_messages_cpp)
target_link_libraries(objectdetect_test ${catkin_LIBRARIES})

add_executable(storing_groc src/storing_groc.cpp)
add_dependencies(storing_groc imgpcl_generate_messages_cpp)
target_link_libraries(storing_groc ${catkin_LIBRARIES})

add_executable(storing_groc1 src/storing_groc1.cpp)
add_dependencies(storing_groc1 imgpcl_generate_messages_cpp)
target_link_libraries(storing_groc1 ${catkin_LIBRARIES})

add_executable(wave_new src/wave_new.cpp)
add_dependencies(wave_new imgpcl_generate_messages_cpp)
target_link_libraries(wave_new ${catkin_LIBRARIES})

add_executable(restaurant_wave src/restaurant_wave.cpp)
add_dependencies(restaurant_wave imgpcl_generate_messages_cpp)
target_link_libraries(restaurant_wave ${catkin_LIBRARIES})

add_executable(ed_naodian_img src/ed_naodian_img.cpp)
add_dependencies(ed_naodian_img imgpcl_generate_messages_cpp)
target_link_libraries(ed_naodian_img ${catkin_LIBRARIES})

add_executable(final_robot_move src/final_robot_move.cpp)
add_dependencies(final_robot_move imgpcl_generate_messages_cpp)
target_link_libraries(final_robot_move ${catkin_LIBRARIES})

add_executable(restaurant_bardetect src/restaurant_bardetect.cpp)
add_dependencies(restaurant_bardetect imgpcl_generate_messages_cpp)
target_link_libraries(restaurant_bardetect ${catkin_LIBRARIES})

add_executable(doordetect src/doordetect.cpp)
add_dependencies(doordetect imgpcl_generate_messages_cpp)
target_link_libraries(doordetect ${catkin_LIBRARIES})

#add_executable(socket2topic_nd src/socket2topic_nd.cpp)
#add_dependencies(socket2topic_nd imgpcl_generate_messages_cpp)
#target_link_libraries(socket2topic_nd ${catkin_LIBRARIES})
