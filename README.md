# pi_io
ROS Node for using Raspberry PI GPIO.

## Node Information
Topics:
* `gpio/input_cmd`:  
  Publishes `pi_io/gpio_input` message sent if one of the monitored GPIO input line goes high.
  
Services:
* `gpio/output_cmd`:  
  Service used to set one of the slected GPIO output lines high or low.
  
## License
Software source and object files are licensed under the Apache License, Version 2.0. See the License for the specific language governing permissions and limitations under the License.
