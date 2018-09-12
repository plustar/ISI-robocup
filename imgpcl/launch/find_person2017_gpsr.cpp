<launch>
<include file="/opt/ros/indigo/share/openni2_launch/launch/primesense_test.launch" />
 <node name="find_person2017_gpsr" pkg="imgpcl" type="find_person2017_gpsr" output="screen" >
 </node>
</launch>
