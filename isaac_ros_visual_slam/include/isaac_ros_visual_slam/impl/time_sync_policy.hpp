#ifndef ISAAC_ROS_VISUAL_SLAM__IMPL__TIME_SYNC_POLICY_HPP_
#define ISAAC_ROS_VISUAL_SLAM__IMPL__TIME_SYNC_POLICY_HPP_

#include <string>
#include <algorithm>
#include <rclcpp/rclcpp.hpp>

namespace nvidia
{

namespace isaac_ros
{
namespace visual_slam
{

typedef enum {
  EXACT,
  APPROXIMATE
} TIME_SYNC_POLICY;

TIME_SYNC_POLICY parseTimeSyncPolicyString(const std::string & str) {
  std::string profile = str;
  // Convert to upper case.
  std::transform(profile.begin(), profile.end(), profile.begin(), ::toupper);
  if (profile == "EXACT") {
    return TIME_SYNC_POLICY::EXACT;
  }
  if (profile == "APPROXIMATE") {
    return TIME_SYNC_POLICY::APPROXIMATE;
  }
  RCLCPP_WARN_STREAM(
    rclcpp::get_logger("parseTimeSyncPolicyString"),
    "Unknown time sync profile: " << profile << ". Returning profile: APPROXIMATE");
  return TIME_SYNC_POLICY::APPROXIMATE;
}


}  // namespace visual_slam
}  // namespace isaac_ros
}  // namespace nvidia

#endif  // ISAAC_ROS_VISUAL_SLAM__IMPL__TIME_SYNC_POLICY_HPP_