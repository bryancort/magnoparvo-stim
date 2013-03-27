# VR Parvo    PRACTICE
#   modified from regular_parvo.sce
#   5/2004  RV
# Parvo
# This "program" has a series of sine wave gratings alternating
# dark green dark red and it switchs this base picture with
# dark red dark green.
#
# Written by Kevin Ehlers (kehlers@crl.ucsd.edu) for
# The Project in Cognitive & Neural Development of UCSD.
#
# 10/12/2003
#     The stimuli has been changed from its original specification.
#        The box is now a 126px x 126px square instead of 128x128.
#        This was done to make the stimuli have an even number of bars
#        The total number of periods was increased from 4 to 4.5
#        which means there are nine bars instead of eight.  This was done
#        to try to eliminate the scrolling effect that some people saw.
#
#        The stimuli colors are _not_ those specified in the sce file.
#        They are overwritten in the pcl file.
#
# 2/23/2004 - Converted to work with EGI system's NetStation.
#  All responses handled by EGI.
#  Port output handled by the serial port.
#
# 3/12/2004 - Gracefully pauses, resumes and quits.
#
# 4/9/2004 - Supports the full EGI interface via the Serial Port.
#
# 5/17/2004 - KE removed the EGI interface and put the
#              normal parallel port interface back.  

# 6/2/2004  MODIFED for UO lumins  PC  
# 6/9/2004  PRACTICE Parvo RV

pcl_file = "parvo_prac_vr.pcl";
default_background_color = 0,0,0;  

screen_height = 768;
screen_width = 1024;
screen_bit_depth = 32;

write_codes=true;
pulse_width=8; 
 
active_buttons=4;
button_codes = 1,2,101,101;

begin;

$tall = 128; # height of picture

picture {} default;
/*
array {
   picture { bitmap { filename =  "duck.bmp";}; x = 0; y = 0; } duck;
   picture { bitmap { filename =  "slowpok.bmp";}; x = 0; y = 0; } slow;
   picture { bitmap { filename =  "snail.bmp";}; x = 0; y = 0; } snail;
   picture { bitmap { filename =  "bro.bmp";}; x = 0; y = 0; } bro;
} old_target_array;    
*/

array {
   picture { bitmap { filename =  "prac_faleav.bmp";}; x = 0; y = 0; } leaf;
   picture { bitmap { filename =  "prac_smiflow.bmp";}; x = 0; y = 0; } flower;
   picture { bitmap { filename =  "prac_tree.bmp";}; x = 0; y = 0; } tree;
} target_array; 

picture { bitmap { filename =  "bro.bmp";}; x = 0; y = 0; } groupshot; 

# add array of pooh characters and group shot here.

# THis array is only 126 bars long instead of the magno which is 128
array {
TEMPLATE "bars.tem" {
   high   colour       name;
   $tall   "0,0,0"   box0;
   $tall   "46,0,0"   box1;
   $tall   "91,0,0"   box2;
   $tall   "133,0,0"   box3;
   $tall   "169,0,0"   box4;
   $tall   "199,0,0"   box5;
   $tall   "221,0,0"   box6;
   $tall   "235,0,0"   box7;
   $tall   "240,0,0"   box8;
   $tall   "235,0,0"   box9;
   $tall   "221,0,0"   box10;
   $tall   "199,0,0"   box11;
   $tall   "169,0,0"   box12;
   $tall   "133,0,0"   box13;
   $tall   "91,0,0"   box14;
   $tall   "46,0,0"   box15;
   $tall   "0,0,0"   box16;
   $tall   "0,29,0"   box17;
   $tall   "0,58,0"   box18;
   $tall   "0,85,0"   box19;
   $tall   "0,108,0"   box20;
   $tall   "0,127,0"   box21;
   $tall   "0,141,0"   box22;
   $tall   "0,150,0"   box23;
   $tall   "0,153,0"   box24;
   $tall   "0,150,0"   box25;
   $tall   "0,141,0"   box26;
   $tall   "0,127,0"   box27;
   $tall   "0,108,0"   box28;
   $tall   "0,85,0"   box29;
   $tall   "0,58,0"   box30;
   $tall   "0,29,0"   box31;
   $tall   "0,0,0"   box32;
   $tall   "46,0,0"   box33;
   $tall   "91,0,0"   box34;
   $tall   "133,0,0"   box35;
   $tall   "169,0,0"   box36;
   $tall   "199,0,0"   box37;
   $tall   "221,0,0"   box38;
   $tall   "235,0,0"   box39;
   $tall   "240,0,0"   box40;
   $tall   "235,0,0"   box41;
   $tall   "221,0,0"   box42;
   $tall   "199,0,0"   box43;
   $tall   "169,0,0"   box44;
   $tall   "133,0,0"   box45;
   $tall   "91,0,0"   box46;
   $tall   "46,0,0"   box47;
   $tall   "0,0,0"   box48;
   $tall   "0,29,0"   box49;
   $tall   "0,58,0"   box50;
   $tall   "0,85,0"   box51;
   $tall   "0,108,0"   box52;
   $tall   "0,127,0"   box53;
   $tall   "0,141,0"   box54;
   $tall   "0,150,0"   box55;
   $tall   "0,153,0"   box56;
   $tall   "0,150,0"   box57;
   $tall   "0,141,0"   box58;
   $tall   "0,127,0"   box59;
   $tall   "0,108,0"   box60;
   $tall   "0,85,0"   box61;
   $tall   "0,58,0"   box62;
   $tall   "0,29,0"   box63;
   $tall   "0,0,0"   box64;
   $tall   "46,0,0"   box65;
   $tall   "91,0,0"   box66;
   $tall   "133,0,0"   box67;
   $tall   "169,0,0"   box68;
   $tall   "199,0,0"   box69;
   $tall   "221,0,0"   box70;
   $tall   "235,0,0"   box71;
   $tall   "240,0,0"   box72;
   $tall   "235,0,0"   box73;
   $tall   "221,0,0"   box74;
   $tall   "199,0,0"   box75;
   $tall   "169,0,0"   box76;
   $tall   "133,0,0"   box77;
   $tall   "91,0,0"   box78;
   $tall   "46,0,0"   box79;
   $tall   "0,0,0"   box80;
   $tall   "0,29,0"   box81;
   $tall   "0,58,0"   box82;
   $tall   "0,85,0"   box83;
   $tall   "0,108,0"   box84;
   $tall   "0,127,0"   box85;
   $tall   "0,141,0"   box86;
   $tall   "0,150,0"   box87;
   $tall   "0,153,0"   box88;
   $tall   "0,150,0"   box89;
   $tall   "0,141,0"   box90;
   $tall   "0,127,0"   box91;
   $tall   "0,108,0"   box92;
   $tall   "0,85,0"   box93;
   $tall   "0,58,0"   box94;
   $tall   "0,29,0"   box95;
   $tall   "0,0,0"   box96;
   $tall   "46,0,0"   box97;
   $tall   "91,0,0"   box98;
   $tall   "133,0,0"   box99;
   $tall   "169,0,0"   box100;
   $tall   "199,0,0"   box101;
   $tall   "221,0,0"   box102;
   $tall   "235,0,0"   box103;
   $tall   "240,0,0"   box104;
   $tall   "235,0,0"   box105;
   $tall   "221,0,0"   box106;
   $tall   "199,0,0"   box107;
   $tall   "169,0,0"   box108;
   $tall   "133,0,0"   box109;
   $tall   "91,0,0"   box110;
   $tall   "46,0,0"   box111;
   $tall   "0,0,0"   box112;
   $tall   "0,29,0"   box113;
   $tall   "0,58,0"   box114;
   $tall   "0,85,0"   box115;
   $tall   "0,108,0"   box116;
   $tall   "0,127,0"   box117;
   $tall   "0,141,0"   box118;
   $tall   "0,150,0"   box119;
   $tall   "0,153,0"   box120;
   $tall   "0,150,0"   box121;
   $tall   "0,141,0"   box122;
   $tall   "0,127,0"   box123;
   $tall   "0,108,0"   box124;
   $tall   "0,85,0"   box125;
};
} boxes;

picture {} pic1;

picture {
   text {
      caption = "Paused...";
      font_size = 42;
      font_color = 255,255,255;
   } pause_text;
   x=0;y=0;
} pause_pic;


trial {
   trial_duration = stimuli_length;
   stimulus_event {
      picture pic1;
      duration = 200;
      code = "switch"; 
#      port_code=99;port=2;
   } main_stim;
} main_trial;

trial {
   trial_duration = stimuli_length;
   stimulus_event {
      picture default;
      duration = 1000;
      code = "isi";
      port_code=1;port=2;
   } isi_stim;
} isi_trial;

trial {
   trial_duration = stimuli_length;
   trial_type = first_response;
   picture pause_pic;
   code = "pause";
   time = 0;
   duration = response;
} pause_trial;  

trial {
   trial_type = fixed;
   picture groupshot;
   time = 0;
   duration = 4000;
} final_pic;