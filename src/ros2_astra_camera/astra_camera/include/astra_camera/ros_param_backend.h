/**************************************************************************/
/*                                                                        */
/* Copyright (c) 2013-2023 Orbbec 3D Technology, Inc                      */
/*                                                                        */
/* PROPRIETARY RIGHTS of Orbbec 3D Technology are involved in the         */
/* subject matter of this material. All manufacturing, reproduction, use, */
/* and sales rights pertaining to this subject matter are governed by the */
/* license agreement. The recipient of this software implicitly accepts   */
/* the terms of the license.                                              */
/*                                                                        */
/**************************************************************************/

#pragma once
#include <rclcpp/rclcpp.hpp>
#include <rcl_interfaces/msg/set_parameters_result.hpp>
#include <functional>
#include <vector>

using ParametersCallback = std::function<rcl_interfaces::msg::SetParametersResult(const std::vector<rclcpp::Parameter>&)>;

namespace astra_camera {
class ParametersBackend {
 public:
  explicit ParametersBackend(rclcpp::Node* node);
  ~ParametersBackend() = default;
  void addOnSetParametersCallback(
      ParametersCallback callback);
      //rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType callback);

 private:
  rclcpp::Node* node_;
  rclcpp::Logger logger_;
  rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr ros_callback_;
  //std::shared_ptr<void> ros_callback_;
};
}  // namespace astra_camera
