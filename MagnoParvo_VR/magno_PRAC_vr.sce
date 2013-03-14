# Magno PRACTICE
# This "program" has a sine wave grating that scrolls from
# left to right.
#
# Written by Kevin Ehlers (kehlers@crl.ucsd.edu) for
# The Project in Cognitive & Neural Development of UCSD.
#
# Pre-Final Version: 9/30/2003
#  The gradient colors are re-defined in the pcl file according
#     to a sine wave based on luminance value instead of
#     "gun voltage" value (0-255).
#
# 2nd-Pre-Final Version: 10/7/2003
#  This now uses the new luminance values.
#
# EGI Version: 2/20/2004
#  Converted to use the serial port to interface with
#  EGI's NetStation.
#
# EGI UPDATE: 3/10/2004
#  Okay, you need to turn on RTS Control in the Port Settings "Advanced" tab
#    for the serial port.
#  Responses are handled by Net Station.
#  
# All responses are handled by EGI.  I.e. the response
# box plugs into the amplifiers
#
# 3/12/2004 - Gracefully pauses, resumes and quits.
#
# 4/2/2004 - See egi_magno.pcl for changes. 

# 6/2/2004  MODIFED for UO luminosity  pec    

# 6/9/2004 Practice version of Magno RV


pcl_file = "magno_prac_vr.pcl";   


default_picture_duration = next_picture;
# The default background color should be changed in the
# pcl file, but for some reason, it keeps on flickering
default_background_color = 245,245,245;

screen_height = 768;
screen_width = 1024;
screen_bit_depth = 32; #32 bit is fine as well

write_codes = true;
pulse_width = 8; # we sample at 250Hz, i.e. 4ms per sample.

active_buttons=4;
button_codes = 1,2,101,101;

begin;

$tall = 128; # height of picture

picture {} default;

picture {} pic1;

picture {
   text {
      caption = "Paused...";
      font_size = 42;
      font_color = 0,0,0;
   } pause_text;
   x=0;y=0;
} pause_pic;

array {
   picture { bitmap { filename =  "prac_faleav.bmp";}; x = 0; y = 0; } leaf;
   picture { bitmap { filename =  "prac_smiflow.bmp";}; x = 0; y = 0; } flower;
   picture { bitmap { filename =  "prac_tree.bmp";}; x = 0; y = 0; } tree;
} target_array;        

picture { bitmap { filename =  "bro.bmp";}; x = 0; y = 0; } groupshot; 


/*
array {
   picture { bitmap { filename =  "bashful.bmp";}; x = 0; y = 0; } bashful;
   picture { bitmap { filename =  "doc.bmp";}; x = 0; y = 0; } doc;
   picture { bitmap { filename =  "dopey.bmp";}; x = 0; y = 0; } dopey;
   picture { bitmap { filename =  "grumpy.bmp";}; x = 0; y = 0; } grumpy;
   picture { bitmap { filename =  "happy.bmp";}; x = 0; y = 0; } happy;
   picture { bitmap { filename =  "sleepy.bmp";}; x = 0; y = 0; } sleepy;
   picture { bitmap { filename =  "sneezy.bmp";}; x = 0; y = 0; } sneezy;
} target_array; 

 picture { bitmap { filename =  "grumpy.bmp";}; x = 0; y = 0; } groupshot;
*/

trial {
   trial_duration = stimuli_length;
   stimulus_event {
      picture pic1;
      code = "pic";
	port_code=1;port=2;
   } main_stim;
} main_trial;

trial {
   trial_duration = stimuli_length;
   stimulus_event {
      picture pic1; 
#      	port_code=99;port=2;
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


# The following array of boxes is there only
# because of the limitations of presentation.
# These values don't really matter.
# They are reset in the pcl file.
array {
TEMPLATE "bars.tem" {
   high   colour       name;
   $tall   "187,187,187"   box0;
   $tall   "189,189,189"   box1;
   $tall   "192,192,192"   box2;
   $tall   "195,195,195"   box3;
   $tall   "198,198,198"   box4;
   $tall   "201,201,201"   box5;
   $tall   "204,204,204"   box6;
   $tall   "207,207,207"   box7;
   $tall   "210,210,210"   box8;
   $tall   "213,213,213"   box9;
   $tall   "215,215,215"   box10;
   $tall   "218,218,218"   box11;
   $tall   "220,220,220"   box12;
   $tall   "223,223,223"   box13;
   $tall   "225,225,225"   box14;
   $tall   "227,227,227"   box15;
   $tall   "230,230,230"   box16;
   $tall   "232,232,232"   box17;
   $tall   "234,234,234"   box18;
   $tall   "235,235,235"   box19;
   $tall   "237,237,237"   box20;
   $tall   "239,239,239"   box21;
   $tall   "240,240,240"   box22;
   $tall   "242,242,242"   box23;
   $tall   "243,243,243"   box24;
   $tall   "244,244,244"   box25;
   $tall   "245,245,245"   box26;
   $tall   "246,246,246"   box27;
   $tall   "246,246,246"   box28;
   $tall   "247,247,247"   box29;
   $tall   "247,247,247"   box30;
   $tall   "247,247,247"   box31;
   $tall   "248,248,248"   box32;
   $tall   "247,247,247"   box33;
   $tall   "247,247,247"   box34;
   $tall   "247,247,247"   box35;
   $tall   "246,246,246"   box36;
   $tall   "246,246,246"   box37;
   $tall   "245,245,245"   box38;
   $tall   "244,244,244"   box39;
   $tall   "243,243,243"   box40;
   $tall   "242,242,242"   box41;
   $tall   "240,240,240"   box42;
   $tall   "239,239,239"   box43;
   $tall   "237,237,237"   box44;
   $tall   "235,235,235"   box45;
   $tall   "234,234,234"   box46;
   $tall   "232,232,232"   box47;
   $tall   "230,230,230"   box48;
   $tall   "227,227,227"   box49;
   $tall   "225,225,225"   box50;
   $tall   "223,223,223"   box51;
   $tall   "220,220,220"   box52;
   $tall   "218,218,218"   box53;
   $tall   "215,215,215"   box54;
   $tall   "213,213,213"   box55;
   $tall   "210,210,210"   box56;
   $tall   "207,207,207"   box57;
   $tall   "204,204,204"   box58;
   $tall   "201,201,201"   box59;
   $tall   "198,198,198"   box60;
   $tall   "195,195,195"   box61;
   $tall   "192,192,192"   box62;
   $tall   "189,189,189"   box63;
   $tall   "187,187,187"   box64;
   $tall   "189,189,189"   box65;
   $tall   "192,192,192"   box66;
   $tall   "195,195,195"   box67;
   $tall   "198,198,198"   box68;
   $tall   "201,201,201"   box69;
   $tall   "204,204,204"   box70;
   $tall   "207,207,207"   box71;
   $tall   "210,210,210"   box72;
   $tall   "213,213,213"   box73;
   $tall   "215,215,215"   box74;
   $tall   "218,218,218"   box75;
   $tall   "220,220,220"   box76;
   $tall   "223,223,223"   box77;
   $tall   "225,225,225"   box78;
   $tall   "227,227,227"   box79;
   $tall   "230,230,230"   box80;
   $tall   "232,232,232"   box81;
   $tall   "234,234,234"   box82;
   $tall   "235,235,235"   box83;
   $tall   "237,237,237"   box84;
   $tall   "239,239,239"   box85;
   $tall   "240,240,240"   box86;
   $tall   "242,242,242"   box87;
   $tall   "243,243,243"   box88;
   $tall   "244,244,244"   box89;
   $tall   "245,245,245"   box90;
   $tall   "246,246,246"   box91;
   $tall   "246,246,246"   box92;
   $tall   "247,247,247"   box93;
   $tall   "247,247,247"   box94;
   $tall   "247,247,247"   box95;
   $tall   "248,248,248"   box96;
   $tall   "247,247,247"   box97;
   $tall   "247,247,247"   box98;
   $tall   "247,247,247"   box99;
   $tall   "246,246,246"   box100;
   $tall   "246,246,246"   box101;
   $tall   "245,245,245"   box102;
   $tall   "244,244,244"   box103;
   $tall   "243,243,243"   box104;
   $tall   "242,242,242"   box105;
   $tall   "240,240,240"   box106;
   $tall   "239,239,239"   box107;
   $tall   "237,237,237"   box108;
   $tall   "235,235,235"   box109;
   $tall   "234,234,234"   box110;
   $tall   "232,232,232"   box111;
   $tall   "230,230,230"   box112;
   $tall   "227,227,227"   box113;
   $tall   "225,225,225"   box114;
   $tall   "223,223,223"   box115;
   $tall   "220,220,220"   box116;
   $tall   "218,218,218"   box117;
   $tall   "215,215,215"   box118;
   $tall   "213,213,213"   box119;
   $tall   "210,210,210"   box120;
   $tall   "207,207,207"   box121;
   $tall   "204,204,204"   box122;
   $tall   "201,201,201"   box123;
   $tall   "198,198,198"   box124;
   $tall   "195,195,195"   box125;
   $tall   "192,192,192"   box126;
   $tall   "189,189,189"   box127;
}; #end template
} boxes; #end picture array

# Presentation does not copy pictures when you type pic1 = pic2; some_stim.set_stim(pic1);
# It duplicates the picture in ram.  IF you then type pic2.clear(); some_stim.set_stim(pic1);
# it will show the default picture...hense the following array...sigh
array {
	picture {} ptemp1;
	picture {} ptemp2;
	picture {} ptemp3;
	picture {} ptemp4;
	picture {} ptemp5;
	picture {} ptemp6;
	picture {} ptemp7;
	picture {} ptemp8;
	picture {} ptemp9;
	picture {} ptemp10;
	picture {} ptemp11;
	picture {} ptemp12;
	picture {} ptemp13;
	picture {} ptemp14;
	picture {} ptemp15;
	picture {} ptemp16;
	picture {} ptemp17;
	picture {} ptemp18;
	picture {} ptemp19;
	picture {} ptemp20;
	picture {} ptemp21;
	picture {} ptemp22;
	picture {} ptemp23;
	picture {} ptemp24;
	picture {} ptemp25;
	picture {} ptemp26;
	picture {} ptemp27;
	picture {} ptemp28;
	picture {} ptemp29;
	picture {} ptemp30;
	picture {} ptemp31;
	picture {} ptemp32;
	picture {} ptemp33;
	picture {} ptemp34;
	picture {} ptemp35;
	picture {} ptemp36;
	picture {} ptemp37;
	picture {} ptemp38;
	picture {} ptemp39;
	picture {} ptemp40;
	picture {} ptemp41;
	picture {} ptemp42;
	picture {} ptemp43;
	picture {} ptemp44;
	picture {} ptemp45;
	picture {} ptemp46;
	picture {} ptemp47;
	picture {} ptemp48;
	picture {} ptemp49;
	picture {} ptemp50;
	picture {} ptemp51;
	picture {} ptemp52;
	picture {} ptemp53;
	picture {} ptemp54;
	picture {} ptemp55;
	picture {} ptemp56;
	picture {} ptemp57;
	picture {} ptemp58;
	picture {} ptemp59;
	picture {} ptemp60;
	picture {} ptemp61;
	picture {} ptemp62;
	picture {} ptemp63;
	picture {} ptemp64;
	picture {} ptemp65;
	picture {} ptemp66;
	picture {} ptemp67;
	picture {} ptemp68;
	picture {} ptemp69;
	picture {} ptemp70;
	picture {} ptemp71;
	picture {} ptemp72;
	picture {} ptemp73;
	picture {} ptemp74;
	picture {} ptemp75;
	picture {} ptemp76;
	picture {} ptemp77;
	picture {} ptemp78;
	picture {} ptemp79;
	picture {} ptemp80;
	picture {} ptemp81;
	picture {} ptemp82;
	picture {} ptemp83;
	picture {} ptemp84;
	picture {} ptemp85;
	picture {} ptemp86;
	picture {} ptemp87;
	picture {} ptemp88;
	picture {} ptemp89;
	picture {} ptemp90;
	picture {} ptemp91;
	picture {} ptemp92;
	picture {} ptemp93;
	picture {} ptemp94;
	picture {} ptemp95;
	picture {} ptemp96;
	picture {} ptemp97;
	picture {} ptemp98;
	picture {} ptemp99;
	picture {} ptemp100;
	picture {} ptemp101;
	picture {} ptemp102;
	picture {} ptemp103;
	picture {} ptemp104;
	picture {} ptemp105;
	picture {} ptemp106;
	picture {} ptemp107;
	picture {} ptemp108;
	picture {} ptemp109;
	picture {} ptemp110;
	picture {} ptemp111;
	picture {} ptemp112;
	picture {} ptemp113;
	picture {} ptemp114;
	picture {} ptemp115;
	picture {} ptemp116;
	picture {} ptemp117;
	picture {} ptemp118;
	picture {} ptemp119;
	picture {} ptemp120;
	picture {} ptemp121;
	picture {} ptemp122;
	picture {} ptemp123;
	picture {} ptemp124;
	picture {} ptemp125;
	picture {} ptemp126;
	picture {} ptemp127;
	picture {} ptemp128;
} pics; #picture array

