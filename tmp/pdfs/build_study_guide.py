from pathlib import Path
import html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/NRL_Programming_Important_Notes.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)
W, H = A4
NAVY = colors.HexColor('#13304A')
TEAL = colors.HexColor('#007D87')
LIGHT = colors.HexColor('#EAF3F5')
GRAY = colors.HexColor('#51606C')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX', fontName='Helvetica-Bold', fontSize=29, leading=34, textColor=NAVY, spaceAfter=18))
styles.add(ParagraphStyle(name='SectionX', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle(name='SubX', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=TEAL, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyX', fontName='Helvetica', fontSize=10.2, leading=14.4, textColor=NAVY, spaceAfter=7))
styles.add(ParagraphStyle(name='SmallX', fontName='Helvetica', fontSize=8.4, leading=11.5, textColor=GRAY, spaceAfter=5))
styles.add(ParagraphStyle(name='CodeX', fontName='Courier', fontSize=8.1, leading=10.6, textColor=NAVY, backColor=LIGHT, borderPadding=8, spaceBefore=5, spaceAfter=9))
styles.add(ParagraphStyle(name='CellX', fontName='Helvetica', fontSize=9, leading=12, textColor=NAVY))
styles.add(ParagraphStyle(name='HeadCellX', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.white))
story=[]
def p(t, style='BodyX'): story.append(Paragraph(t, styles[style]))
def h(t): p(t,'SubX')
def page(title, source):
    if story: story.append(PageBreak())
    p(title,'SectionX'); p(source,'SmallX')
def bullet(t): p('• '+t)
def box(title,t):
    a=Table([[Paragraph('<b>'+title+'</b><br/>'+t,styles['BodyX'])]],colWidths=[W-92])
    a.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),.7,TEAL),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.extend([a,Spacer(1,9)])
def table(headers, rows, widths):
    cells=[[Paragraph(html.escape(x),styles['HeadCellX']) for x in headers]]
    cells += [[Paragraph(x,styles['CellX']) for x in row] for row in rows]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,NAVY),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]))
    story.extend([t,Spacer(1,7)])
def code(s): story.append(Preformatted(s.strip(),styles['CodeX']))

p('NRL PROGRAMMING / STUDY GUIDE','SmallX')
p('The important parts,<br/>in course order.','TitleX')
p('A practical guide to all <b>28 programming modules</b> in the NRL portal, with extra attention to your four-wheel robot, gripper and lifting arm.')
box('Read this first','The controller sends your inputs. The robot runs your OpMode and commands its hardware. Seeing a program name on the controller does not prove that INIT or START has happened.')
table(['Course phase','What you need to learn','Pages'],[
('1 / Foundations','C++ values, decisions, repetition and functions.','3-4'),
('2 / Getting Started','Project files, upload, connection and pairing.','5-6'),
('3 / Programming the Robot','Drive, servos, buttons, sensors and feedback.','7-11'),
('4 / Autonomous & Advanced','Responsive sequences, turns and motion tuning.','12-13'),
('5 / Reference & Practice','Diagnosis, API reminders and learning sequence.','14-18')],[114,335,54])
h('What to prioritize for your robot')
p('<b>First:</b> the program lifecycle (page 2), upload/pairing (pages 5-6), and the button map (page 6). <b>Then:</b> servo motion and your saved program (pages 8-9). Use the troubleshooting page before changing wiring or code blindly.')
h('How these notes were checked')
p('The live programming curriculum was reviewed through its final lesson, 5.5, on 16 October 2026. Important API and button details were compared with the SDK files in your project. This is an original study summary, not a copy of the course.')
p('<b>Scope:</b> all five programming phases. The portal also has mechanical and electronics curricula; those are outside this programming guide. Hardware motion and mechanical endpoints remain unverified.','SmallX')

page('The order every robot program follows','Core reference: Modules 2.1, 2.5, 4.1; installed NRLOpMode.h')
table(['Order','What belongs here'],[
('1. Includes and settings','Load NRL.h and any helper headers. Give speeds, pins and angles meaningful names.'),
('2. Hardware and state','Declare motor/servo objects, TankDrive, and values that must persist between loop calls.'),
('3. init()','Prepare the hardware once. Check begin() results. Keep wheel commands stopped. Servo begin() can physically move to its start angle.'),
('4. start()','Reset timers and run state. Queue a one-time autonomous sequence here.'),
('5. loop()','Read inputs, decide what to do, issue commands and report telemetry. Return quickly so the framework can keep working.'),
('6. stop()','Stop the drive and any independent motors. Deliberately choose whether mechanisms hold or release, accounting for framework cleanup.'),
('7. REGISTER_OPMODE','Give the class a controller menu name and TELEOP or AUTO type.')],[126,377])
box('An important course correction','The course says nothing should move during INIT, but HexaServo.begin() commands its start angle. Your full robot program initializes both servos at 90 degrees during INIT. Treat that as a real movement, not a harmless setup step.')
h('Repeated loop does not mean automatic back-and-forth')
p('The framework calls loop() repeatedly. It can keep checking whether OPEN or CLOSE is held; it does not need a blocking while(true). A repeating open/close sequence would be a different behavior.')
p('The installed SDK describes a roughly 100 Hz loop, TELEOP duration of 2 minutes 30 seconds, and AUTO duration of 60 seconds. These are software defaults, not a statement of current competition rules.')
p('<b>Keep it responsive:</b> avoid delay(), long waits and loops that wait for a button or sensor. Actions or elapsed-time checks allow STOP, radio input and telemetry to keep being serviced.')

page('Phase 1 / C++ essentials','Modules 1.1 Introduction to C++; 1.2 Variables & Data Types; 1.3 Operators')
h('A small vocabulary that explains most code')
table(['Code idea','Meaning and robot use'],[
('Variable','A named value: current angle, timer or button state. Initialize it before reading it.'),
('int / uint32_t','Whole-number counts; uint32_t is useful for millisecond timestamps.'),
('float','A number with a fractional part, such as 0.5f drive power or 10.0f degrees per second.'),
('bool','true or false: paused, connected, hardware ready or button held.'),
('char / string','One character uses single quotes; a text literal uses double quotes.'),
('const / constexpr','A value intended to stay fixed, such as a calibrated endpoint.'),
('Semicolons and braces','A semicolon ends a statement; braces group a function or decision body.')],[120,383])
code('''const float OPEN_ANGLE = 90.0f;
float commandedAngle = OPEN_ANGLE;
bool paused = false;
commandedAngle += 1.0f;  // change a stored value''')
h('Operators you will use constantly')
p('<b>=</b> stores a value; <b>==</b> compares values. <b>!=</b> means different. Use &lt;, &lt;=, &gt; and &gt;= for limits. <b>&amp;&amp;</b> means both conditions, <b>||</b> means either condition, and <b>!</b> means not.')
p('Arithmetic uses +, -, *, / and % (integer remainder). Use parentheses when combining conditions or calculations. With integers, 5 / 2 gives 2; 5.0f / 2 gives 2.5. This matters when converting milliseconds into seconds.')
h('Desktop C++ versus robot C++')
p('The first lessons use main(), cout and cin to learn the language. A robot OpMode instead uses the NRL framework, gamepad1 and telemetry. You normally do not add a second main() to the robot project.')
p('A successful compile catches syntax and type problems. It cannot prove that the right wheel turns forward, that the correct program started, or that a servo angle is safe.')

page('Phase 1 / Decisions, loops and functions','Modules 1.4 Conditionals & Loops; 1.5 Functions & Scope')
h('Decide in a clear priority order')
code('''if (!hardwareReady) {
    // Report the setup failure.
} else if (linkLost || paused) {
    // Stop the drive; freeze mechanism targets.
} else {
    // Use the driver's current inputs.
}''')
p('An if / else-if chain runs the first matching branch. Put conditions that must override driving before normal commands. A switch is useful for named stages of a routine; use break so execution does not fall into the next case.')
h('Understand the three kinds of repetition')
table(['Structure','Use'],[
('for','A known, short amount of work, such as checking a small array.'),
('while / do-while','Repeat while a condition is true. A do-while runs at least once. Do not use either to wait indefinitely inside robot callbacks.'),
('NRL loop()','The framework repeatedly calls this function. Read the current state and return; let the next call handle the next moment.')],[133,370])
h('Functions make the order easier to read')
p('A function groups a job, accepts parameters and may return a result. void means no returned value. Use helpers for tasks such as calculating a new servo target or stopping all outputs. Define a function before use, or provide a declaration.')
p('A local variable exists inside its function or block. A timer declared fresh inside loop() does not automatically remember the previous call. Store persistent angles, flags and timestamps as class members. A file-scope static object is another pattern used by the lessons.')
h('Frequent mistakes')
bullet('Using = when you meant ==; forgetting braces or a semicolon; placing an accidental semicolon immediately after if or for.')
bullet('Using an uninitialized value, mixing up seconds and milliseconds, or changing a loop boundary by one iteration.')
bullet('Toggling a state every loop while a button is held. Use justPressed() for a one-time toggle.')

page('Phase 2 / Project, build and upload','Modules 2.1-2.4; Module 2.5 Flashing and Pairing')
table(['Part','Its role'],[
('Robot Command Hub','Executes OpModes and drives the hardware. This is where your gripper and drive logic belongs.'),
('Handheld controller','Runs the menu and screen, reads buttons/sticks and sends input over ESP-NOW.'),
('VS Code + PlatformIO','Edit, compile and upload robot firmware. First setup may download dependencies.'),
('Project workspace','Open the generated .code-workspace so the robot and controller folders are easy to find.')],[137,366])
h('Files to recognize in your project')
p('<b>RobotFirmware/opmodes/</b> holds robot programs. <b>RobotFirmware/platformio.ini</b> holds build settings. <b>lib/</b> supplies hardware libraries. <b>ControllerFirmware/</b> contains the supplied controller image and its flasher. Use BoardPins.h names such as SERVO_1 rather than guessed GPIO numbers.')
h('The edit-to-run sequence')
bullet('<b>Save:</b> make a small change and keep a numbered source snapshot.')
bullet('<b>Build:</b> compile the robot environment and fix errors. A successful build does not upload anything.')
bullet('<b>Upload:</b> connect the intended board with a USB data cable, select its actual port, and use the matching upload workflow. A charge-only cable is insufficient.')
bullet('<b>Verify:</b> read the upload success result, check connection/pairing, select the program, then follow INIT and START. Check telemetry from the running program.')
box('Your controller uses a supplied image','In this kit, robot code is built with PlatformIO; the controller is flashed with ControllerFirmware/flash_controller.py. You do not need a controller reflash for each change to a robot OpMode. The kit does not supply editable controller application source.')
h('Avoid a misleading shortcut')
p('An application firmware.bin alone is not necessarily a complete flash image. Use the project upload tools, which know the required partitions and offsets. If a port is busy, close its serial monitor before uploading. Do not infer the board from a COM number alone after reconnecting.')

page('Phase 2 / Pairing and physical controls','Module 2.5; Module 3.4; user-supplied controller diagram; installed NRLGamepad.h')
p('Both boards must use the same radio channel. Your saved project uses <b>channel 6</b>. ESP-NOW connects the devices directly; a home Wi-Fi router is not required.')
p('<b>Course pairing sequence:</b> hold the robot pairing button for about 3 seconds; in the controller pairing menu hold both shoulder bumpers (LB + RB); compare the displayed four-digit codes; hold the robot button for about 1 second to confirm. Pairing is remembered. Follow the actual prompts if firmware wording differs.')
diagram=Path('C:/Users/gamer/AppData/Local/Temp/codex-clipboard-c2365b6d-d33b-4ce1-a7d9-1567e8ad9798.png')
if diagram.exists():
    story.append(Image(str(diagram),width=490,height=490*679/1027))
p('Controller diagram supplied in this conversation. Shoulder bumpers and top toggle switches are separate controls.','SmallX')
table(['Physical label','Code / behavior'],[
('SELECT / X','Upper left face button nearest the screen. Selects in menus; your running program uses it for gripper open.'),
('BACK / Y and HOME / A','Y is the middle left face button. A is the lowest, farthest left. Your program uses A for gripper close.'),
('D-pad / LB / RB','Four right-side buttons; left/right shoulder bumpers. Their running behavior is assigned by the OpMode.'),
('TOP-LEFT TOGGLE / LT','In the supplied controller version, opens the exit confirmation. Follow the screen to exit.')],[147,356])
p('<b>Version correction:</b> course tables saying Y is always STOP, or listing a B button, do not match this project. The installed header says Y is available while running and this board has no B button. Do not guess a physical START button; follow the displayed INIT/START prompts.','SmallX')

page('Phase 3 / Motors and driving','Modules 3.1 Motors; 3.2 Driving with TankDrive; 4.4 control concepts')
h('Two different command scales')
table(['API','Meaning'],[
('motor.setSpeed(value)','Signed command from -255 to +255. Zero coasts. The sign determines the commanded direction.'),
('drive.drive(forward, turn)','Two normalized inputs, each from -1 to +1. TankDrive combines them into left/right wheel commands.'),
('drive.setScale(value)','A drive-power factor from 0 to 1; useful for beginner and precision modes.'),
('drive.setRampRate(value)','Controls change per update in this SDK. This is not a servo degrees-per-second value.'),
('motor.getSpeed()','Returns a command value, not a measured wheel RPM.'),
('drive.stop() / motor.stop()','Use in stop() and in conditions that require the wheels to stop.')],[171,332])
code('''// Inside loop(): left stick = forward, right stick = turn.
drive.drive(gamepad1.leftY(), gamepad1.rightX());''')
p('Construct motors using MOTOR_L_DIR/MOTOR_L_PWM and MOTOR_R_DIR/MOTOR_R_PWM, then construct TankDrive from those motors. Call each motor\'s begin() in init(). A motor flip setting compensates for physical mounting or wiring direction.')
h('Four wheels do not prove four independent software channels')
p('Your photo shows four motor connections and you said each wheel has its own plug. The production SDK exposes left and right drive channels. That does not establish the electrical grouping of the sockets. Verify which wheels respond to each side before relying on the assumed front/rear grouping. Do not use bench-only MOTOR_3/MOTOR_4 definitions as production outputs.')
h('Tune from a controlled starting point')
bullet('Check directions with the wheels raised and a low command. Reverse the appropriate side in settings if needed.')
bullet('Start with a reduced drive scale. Use a deadband so tiny stick noise does not cause creep.')
bullet('Use acceleration ramping to reduce abrupt current demand. A reset under load also requires checking battery condition and connections.')
p('The course uses different flipped sides in different examples. Choose the setting from the actual wheel response, not from a copied example.')

page('Phase 3 / Servo angles and slow movement','Module 3.3 Servos; installed HexaServo driver; your requested behavior')
table(['Concept','What it really means'],[
('setPosition(90)','An absolute servo command. It does not mean rotate another 90 degrees.'),
('moveBy(10)','A relative change to the current software angle.'),
('begin()','Initializes the servo and commands its configured start angle. The first physical movement can be fast.'),
('getPosition()','The last written software angle; not a sensor reading of the actual shaft.'),
('setRampRate(10.0f)','The SDK offers output ramping in degrees per second. Set before position commands; it cannot discover an unknown initial shaft angle.'),
('settleMs = 0 / detach()','Zero keeps the servo signal active to hold position. Detach releases holding torque; an arm can drop.')],[156,347])
h('Your 10 degrees per second requirement')
p('Change the <b>commanded angle</b> according to elapsed time: <b>change = 10 x elapsed milliseconds / 1000</b>. A 90-degree command change takes about 9 seconds; 45 degrees takes about 4.5 seconds. Real motion can differ with load, voltage and servo behavior.')
code('''// Algorithm fragment, not a standalone OpMode.
float step = 10.0f * elapsedMs / 1000.0f;
// OPEN only: increase target by step, capped at open endpoint.
// CLOSE only: decrease target by step, capped at closed endpoint.
// Neither or both: keep the target unchanged.
// Write the target only when it changes.''')
p('Your full program implements this elapsed-time approach and caps delayed updates at 100 ms to avoid a large catch-up jump. Keep one layer responsible for motion timing; stacking two unrelated ramps makes the result harder to understand.')
box('Calibrate the mechanism, not just the number','Gripper 0/90 and arm 45/90/135 are trial commands. A photo does not identify a safe angle or rotation direction. Start at a supported pose, use small changes, observe linkage clearance and record the actual endpoints. Clockwise versus anticlockwise depends on viewing direction and mounting.')
p('Keep the driver\'s normal angle-to-pulse mapping. Clamp your application targets to calibrated limits; do not assume changing driver minAngle/maxAngle is equivalent to adding a mechanical safety clamp.')

page('Your robot / Saved program and controls','Application of Modules 3.1-3.4; GalaxyTeleOp.cpp, GalaxySettings.h, GalaxyMotion.h')
p('<b>Galaxy TeleOp</b> is the full robot program. It uses servo 1 for the gripper and servo 4 for the lifting arm. Its numbered course-order revision is saved as <b>005</b>. It has not been uploaded as part of this study-guide task. The last previously verified upload remains <b>003, Gripper Slow</b>.')
table(['Control','Full robot program behavior'],[
('Left joystick up/down','Forward and reverse.'),
('Right joystick left/right','Turn left and right.'),
('Hold SELECT (X)','Increase gripper target toward 90 degrees (trial open).'),
('Hold HOME (A)','Decrease gripper target toward 0 degrees (trial closed).'),
('Hold D-pad up / down','Move arm toward 135 / 45 degrees; trial neutral is 90.'),
('Release / opposing buttons','Hold the last servo target. Opposing directions cancel.'),
('Hold left bumper (LB)','20% precision drive limit; normal limit is 50%.'),
('Hold right bumper (RB)','Pause wheel motion and freeze servo targets.'),
('Top-left toggle','Open exit confirmation. Confirming exit stops motors and releases servos.')],[170,333])
h('What happens in order')
p('<b>INIT:</b> initialize servos before motors as required by this kit; both servos receive their trial 90-degree starting commands. <b>START:</b> reset timing and require neutral inputs. <b>RUN:</b> read inputs, check readiness/link/pause, move permitted outputs, then report status. <b>STOP:</b> stop motors and release servos.')
p('After START, a link interruption or a pause, center the driving sticks and release the gripper/arm buttons and RB. The program then leaves RELEASE INPUTS and enters RUNNING. Physical travel and safe endpoints still need testing.')
box('Why SELECT may appear to do nothing','In the earlier Gripper Slow test, the first fresh direction press initializes the target at 90 degrees. SELECT cannot increase a target that is already at its 90-degree limit. Check the displayed target and try the opposite direction within the mechanism\'s safe range.')
p('Gripper Slow intentionally delays servo initialization until a fresh button press; it is a diagnostic exception to the course\'s usual begin()-in-init pattern. The full Galaxy TeleOp program uses the course pattern.')

page('Phase 3 / Buttons, IMU and heading','Modules 3.4 The Gamepad; 3.5 The Motion Sensor (IMU) & Heading')
h('Choose the correct kind of button check')
table(['Method','Use it for'],[
('pressed(BTN_X)','A held action: keep moving the target while SELECT is down.'),
('justPressed(BTN_X)','One event on the press edge: toggle a pose or launch one sequence.'),
('justReleased(BTN_X)','One event on release: finish a gesture or release-triggered action.'),
('leftY(), rightX(), etc.','Joystick axes in the -1 to +1 range; apply appropriate deadband and limits.')],[181,322])
p('gamepad1 is the per-loop input interface. If you flip a boolean using pressed(), a long press flips it many times. If you need continuous slow motion, justPressed() alone is insufficient: use the held state plus elapsed time.')
h('Use framework heading when that is all you need')
table(['Method','Meaning'],[
('NRLComms::getHeading()','Read heading in degrees.'),
('NRLComms::zeroHeading()','Make the current direction the reference zero.'),
('NRLComms::isHeadingReady()','Check whether heading calibration is ready.')],[221,282])
p('Let the robot remain still during initial calibration, roughly half a second in the lesson. Heading from a gyro can drift. Zeroing the heading establishes a local reference; it does not create an absolute compass direction.')
h('When you need raw motion readings')
p('A custom HexaIMU uses the board configuration helper and begin(). Keep its calibration progressing through tick(millis()) instead of waiting in a blocking loop. Refresh readings before using acceleration or angular-rate values.')
p('Acceleration is expressed in metres per second squared; a stationary flat sensor sees gravity on its vertical axis, approximately 9.81 m/s² in magnitude. Gyroscope rates use radians per second; heading uses degrees. Do not mix these units.')
box('Readiness is different from accuracy','A ready flag says calibration completed. It does not prove the robot stayed still, the reference is correct or later turns will be exact. Verify heading behavior before building a longer autonomous route.')

page('Phase 3 / Make the robot explain itself','Modules 3.6 Telemetry; 3.7 Status LED; 3.8 OLED; 3.9 Power & Battery')
h('Telemetry is your first diagnostic tool')
p('telemetry.addData(key, value) sends a named value to the controller. Reusing a key updates that item. Keep a small set of clear fields: program/version, lifecycle state, input, commanded angle, link freshness and battery voltage. The lesson gives limits of 64 keys, 11 characters per key and 15 per value.')
code('''telemetry.addData("status", "RUNNING");
telemetry.addData("grip target", commandedAngle);
telemetry.addData("battery V", power.getBatteryVoltage());''')
p('Name values honestly: a target angle is a command, a scale is a power limit, and getSpeed() is not measured speed. Visible changing inputs plus an unchanged output can isolate a logic or endpoint issue.')
h('LED and OLED')
table(['Output','Important workflow'],[
('userLed','Use setSolid, setBlink, setPulse or setOff for your program state. RGB components run from 0 to 255. The framework owns botLed.'),
('HexaOLED','Use the board configuration helper and check begin(). Clear, position the cursor, print/draw, then call display() to show the buffer.'),
('Display refresh','Update at a readable rate instead of redrawing excessively. The course OLED example uses a slower display update than the robot control loop.')],[127,376])
h('Battery and current measurements')
table(['Reading','Interpretation'],[
('getBatteryVoltage() / isBatteryLow()','Pack voltage and the configured low-battery indication.'),
('getMainCurrent()','Total main-rail current.'),
('getMotorCurrent()','Combined motor branch current, not a separate reading for each wheel.'),
('getServoCurrent()','Derived estimate: main current minus motor current; not an individual servo sensor.'),
('readChannelVoltage(ADC_EXT_1)','An external analog input, using the named board constant.')],[218,285])
p('Treat unverified current calibration as approximate. A 10.5 V threshold in an example is not a universal battery rule. Use the pack requirements and configured limits. Servo buzzing can have electrical or mechanical causes; it is not proof that the linkage is moving correctly.','SmallX')

page('Phase 4 / Autonomous sequences','Modules 4.1 Writing an Autonomous OpMode; 4.2 The Action System')
h('Queue once, keep the loop responsive')
p('Register the program as AUTO. Prepare hardware in init(), queue the sequence in start(), use loop() for monitoring, and stop outputs in stop(). An Action spreads work across updates instead of freezing the program.')
table(['Action helper','Meaning'],[
('instant(function)','Run a short command once.'),
('sleep_ms(500)','Let 500 ms pass without blocking the action scheduler.'),
('wait_until(condition)','Wait for a condition to become true; ensure the routine has a sensible timeout or exit path.'),
('sequential({ ... })','Finish steps in order.'),
('parallel({ ... })','Run steps together and finish when all finish.'),
('repeat(action)','Repeat work until cancellation, STOP or the applicable deadline.')],[184,319])
code('''// Fragment inside an AUTO class; drive is already declared.
void start() override {
    runAction(sequential({
        instant([this]{ drive.drive(0.3f, 0.0f); }),
        sleep_ms(500),
        instant([this]{ drive.stop(); })
    }));
}''')
p('The capture [this] allows the inline function to use a drive object stored in the OpMode class. The lessons often use [] because their hardware objects are at file scope. Match the capture to where your object lives.')
box('Do not enqueue the routine on every loop call','The installed SDK adds actions to a queue (up to eight); it does not replace the existing action as one lesson implies. Repeated queueing can overlap commands and fill the queue. Use start() for a one-time AUTO, or justPressed() for a TeleOp trigger.')
p('Give each mechanism one command owner. Actions run before loop() in this kit, so loop() can overwrite an action\'s command. Guard manual control while a sequence owns that mechanism. cancelActions() removes work but does not itself stop motors.')
p('Prefer runAction(). runBlocking() has framework stop checks but holds the calling function until completion. Use the non-blocking approach for normal programs.')

page('Phase 4 / Reliable motion and feedback','Modules 4.3 Precise Motion with DriveActions; 4.4 A Gentle Look Under the Hood')
table(['DriveActions command','Use and limitation'],[
('turn(90)','Relative right turn by 90 degrees; negative turns left. Uses IMU feedback.'),
('turnTo(180)','Aim for an absolute heading in the current reference frame.'),
('driveInches(24)','Estimated distance using a timed model with heading help. It is not wheel-encoder distance measurement.'),
('driveForMs(1500)','Time-based forward movement; distance depends on actual speed and conditions.'),
('waitForHeadingReady()','Allow heading calibration before motion.'),
('stopAll()','Create a drive stop action.'),
('auto_()...build()','Build a sequence by chaining named movement steps.')],[196,307])
h('Build a routine in small pieces')
bullet('Wait for heading readiness while the robot is stationary.')
bullet('Verify a short straight movement; measure actual travel on the intended surface.')
bullet('Verify a relative turn and check its direction and overshoot.')
bullet('Combine the verified steps, include stops, then retest with the expected battery condition and payload.')
h('Four ideas worth remembering')
table(['Idea','Practical meaning'],[
('Deadband','Ignore tiny noise around a neutral input.'),
('Ramping','Change commanded power gradually to reduce jerk and current surges.'),
('Open-loop','Issue a command without measuring the final result. Timed distance changes with traction, battery and load.'),
('Closed-loop','Measure an error and correct it. IMU turns use heading feedback, but are still affected by calibration and drift.')],[119,384])
box('Precision has limits','The course robot has no wheel encoders for its distance model. A requested 24 inches is an estimate, not a measured guarantee. Keep turn calibration and straight-distance calibration separate.')
p('For a simple timed routine without Actions, use unsigned elapsed time: now - startedAt. A state number and a step-start timestamp let each stage have its own duration. Use real time, not an assumed count of loop calls.')

page('Phase 5 / Troubleshoot in this order','Modules 5.1 Worked Examples; 5.2 Common Mistakes & Troubleshooting; project observations')
table(['Symptom','First useful check'],[
('Program name absent','Confirm REGISTER_OPMODE spelling, robot build and upload success. The controller list comes from the robot.'),
('Name appears but will not start','Distinguish menu selection, INIT and START. Observe the controller prompt and lifecycle telemetry/serial messages. Advertising a name is not evidence of START.'),
('No running status','Confirm the intended OpMode actually started before blaming the input or servo.'),
('Status runs; button never changes','Check the physical button map, current connection and firmware-compatible names.'),
('Button changes; target stays fixed','Check upper/lower endpoint, both-buttons-held behavior, pause state and neutral-input requirement.'),
('Target changes; mechanism does not','Check begin() success, correct servo port, connector orientation, power and mechanical binding. The target is not physical feedback.'),
('Abort just after INIT','Check for blocking setup and reported hardware initialization failure.'),
('Twitching or repeated sequences','Check for runAction() inside every loop call, conflicting command owners or a held-state toggle.'),
('Reset when motors start','Check battery/connections and acceleration demand. Reduce command scale and use ramping.'),
('Wrong wheel or turn direction','Verify physical channel mapping and per-side reversal before changing mixing logic.'),
('Poor autonomous turn','Check calibration while still, heading readiness, zero reference and later gyro drift.'),
('Unresponsive after repeated runs','Inspect logs and resource cleanup; a reboot is a diagnostic step, not a substitute for finding the cause.')],[156,347])
h('Use a known example to isolate one subsystem')
p('The course points to Servo Sweep, Motor Ramp, OLED Live and AUTO Live. Test one function at a time before combining drive, arm and gripper. Read the actual code: the short Motor Ramp snippet in 3.1 only ramps upward and the ArmToggle snippet in 3.3 repeatedly commands 90 degrees; their names/descriptions promise more than those snippets implement.')
p('<b>Your unresolved symptom:</b> an earlier capture showed program advertising but no program START message during that capture. This does not identify the cause. A fresh view of the controller prompt plus lifecycle output is the next useful evidence.','SmallX')

page('Phase 5 / API desk reference','Module 5.3 API Quick Reference, corrected against the installed SDK')
table(['Task','Names to recognize'],[
('Program lifecycle','init(), start(), loop(), stop(); REGISTER_OPMODE(Class, "Menu", TELEOP/AUTO)'),
('Motor','HexaDCMotor; begin(), setSpeed(), getSpeed(), stop(), setFlipped()'),
('Drive','TankDrive(left, right); drive(), stop(), setScale(), setRampRate()'),
('Servo','HexaServo; begin(), setPosition(), moveBy(), getPosition(), setRampRate(), attach(), detach()'),
('Controller input','gamepad1.leftY(), rightX(), leftX(), rightY(); pressed(), justPressed(), justReleased()'),
('Face and direction buttons','BTN_X, BTN_A, BTN_Y; BTN_DPAD_UP, BTN_DPAD_DOWN, BTN_DPAD_LEFT, BTN_DPAD_RIGHT'),
('Shoulder controls','BTN_LB, BTN_RB, BTN_LT, BTN_RT. Physical toggles are distinct from bumpers; LT has the controller exit role.'),
('Heading','NRLComms::getHeading(), zeroHeading(), isHeadingReady()'),
('Telemetry','telemetry.addData("key", number_or_text)'),
('User LED','userLed.setSolid(), setBlink(), setPulse(), setOff()'),
('Power','power.getBatteryVoltage(), isBatteryLow(), getMainCurrent(), getMotorCurrent(), getServoCurrent()'),
('Actions','runAction(), isActionRunning(), cancelActions(); instant(), sleep_ms(), wait_until(), sequential(), parallel(), repeat()'),
('Autonomous drive','DriveActions; turn(), turnTo(), driveInches(), driveForMs(), waitForHeadingReady(), auto_()')],[136,367])
h('Values and units at a glance')
p('<b>Motor command:</b> -255 to +255. <b>Joystick/drive inputs:</b> -1 to +1. <b>Drive scale:</b> 0 to 1. <b>Servo command:</b> degrees within your calibrated range. <b>Servo ramp:</b> degrees/second. <b>Timing:</b> milliseconds (1000 ms = 1 second). <b>Voltage:</b> V. <b>Current:</b> A. <b>Heading:</b> degrees.')
p('This reference lists names, not every function overload or configuration field. Check the project header when the lesson and compiler disagree. Never add BTN_B simply to make an outdated example look complete.')

page('Code structure / A readable learning example','Original instructional example following the course order; no motor or servo commands')
p('This small OpMode demonstrates lifecycle and button reporting before connecting input to movement. It uses the same order as the full robot program. Its source is saved separately under study-examples; it is not included in the robot upload.')
code('''#include "NRL.h"

// 1. Hardware declarations would go here.
class CourseInputCheck : public NRLOpMode {
    // 2. State remembered between loop calls.
    uint32_t startedAt = 0;

public:
    // 3. Prepare once when INIT is requested.
    void init() override {
        HexaDCMotor::stopAll();
        telemetry.addData("status", "INIT READY");
    }

    // 4. Reset timing once when START is requested.
    void start() override {
        startedAt = millis();
    }

    // 5. Read inputs and report; return promptly.
    void loop() override {
        telemetry.addData("status", "RUNNING");
        telemetry.addData("SELECT", 
            gamepad1.pressed(BTN_X) ? "DOWN" : "UP");
        telemetry.addData("HOME",
            gamepad1.pressed(BTN_A) ? "DOWN" : "UP");
        telemetry.addData("seconds",
            (millis() - startedAt) / 1000.0f);
    }

    // 6. Clean up once when the program stops.
    void stop() override {
        HexaDCMotor::stopAll();
    }
};

// 7. Publish the menu entry and program type.
REGISTER_OPMODE(CourseInputCheck, "Course Inputs", TELEOP);''')
p('The full GalaxyTeleOp.cpp follows this layout with hardware declarations, initialization checks, drive and servo logic, telemetry and output cleanup. Helper methods are kept below the lifecycle callbacks so init/start/loop/stop read in course order.','SmallX')

page('Phase 5 / Practice, glossary and saved work','Modules 5.1 Worked Examples; 5.4 Glossary; 5.5 Conclusion & Next Steps')
h('A useful practice sequence')
bullet('<b>1. Inputs:</b> show SELECT/HOME and joystick states on telemetry.')
bullet('<b>2. One servo:</b> establish a safe start pose and small movements; record endpoints.')
bullet('<b>3. Slow held control:</b> open and close only while the corresponding button is held.')
bullet('<b>4. Drive:</b> verify side mapping, direction, low-power movement and stop behavior.')
bullet('<b>5. Combine:</b> add the lifting arm, pause, link-loss handling and neutral restart.')
bullet('<b>6. Autonomous:</b> calibrate heading, verify one turn and one short straight move, then sequence them.')
table(['Term','Plain meaning'],[
('OpMode / TeleOp / AUTO','One selectable robot program / driver-controlled mode / timed autonomous mode.'),
('SDK / framework / API','The software kit / the system running your code / its available commands.'),
('Firmware / build / flash','Compiled board software / create it from source / transfer it to a board.'),
('ESP-NOW / pairing','The direct radio link / choosing the particular robot and controller that communicate.'),
('IMU / heading','A motion sensor / the robot\'s current orientation relative to its reference.'),
('Telemetry / state','Live diagnostic values / the program\'s current condition or stage.'),
('PWM / LEDC','Timed pulses used for outputs / the ESP32 hardware generating those signals.'),
('Brownout','A reset caused by insufficient supply voltage under demand.')],[145,358])
h('Save enough to reproduce a working version')
p('Keep the source, settings, firmware image, build result, controller version and a note of tested behavior. Store previous .cpp files outside the active opmodes folder so they are not compiled again. Your earlier snapshots 001-004 are preserved; 005 records the course-order revision.')
p('Every successful test should answer one question. Record which button, port, angle and visible result were tested. A passing build is a software check; a verified upload is a transfer check; neither is a physical movement test.')

page('Coverage, sources and version differences','All 28 programming modules reviewed in the live portal on 16 October 2026')
table(['Modules reviewed','Where summarized'],[
('1.1 Introduction to C++; 1.2 Variables & Data Types; 1.3 Operators','Page 3'),
('1.4 Conditionals & Loops; 1.5 Functions & Scope','Page 4'),
('2.1 Welcome to NRL; 2.2 Installing the Software; 2.3 Creating Your Own Project (HexaSDK); 2.4 Understanding Your Hardware; 2.5 Flashing and Pairing','Pages 2, 5-6'),
('3.1 Motors; 3.2 Driving with TankDrive; 3.3 Servos; 3.4 The Gamepad','Pages 6-10'),
('3.5 The Motion Sensor (IMU) & Heading; 3.6 Telemetry; 3.7 The Status LED; 3.8 The OLED Display; 3.9 Power & Battery','Pages 10-11'),
('4.1 Writing an Autonomous OpMode; 4.2 The Action System; 4.3 Precise Motion with DriveActions; 4.4 A Gentle Look Under the Hood','Pages 12-13'),
('5.1 Worked Examples; 5.2 Common Mistakes & Troubleshooting; 5.3 API Quick Reference; 5.4 Glossary; 5.5 Conclusion & Next Steps','Pages 14-17')],[393,110])
h('Primary course source')
p('<link href="https://nrlportal.theinnovationstory.com/#/youth-dashboard" color="#007D87">NRL Portal - Programming Curriculum</link>. The portal uses one dashboard URL for its chapters; use the module numbers above to locate the relevant lesson. The final programming lesson observed was 5.5. Portal-wide progress also counts other curricula.')
h('Local checks used for practical corrections')
p('RobotFirmware/lib/HexaNRL/src/NRLGamepad.h and NRLOpMode.h; lib/HexaServos/src/HexaServo.h; the project README; CONTROLS.md; ROBOT_GUIDE.md; GalaxyTeleOp.cpp and its settings/helpers. The controller drawing and robot configuration came from your supplied material. These files describe this kit, not every future release.','SmallX')
box('Differences to remember','Use the top-left toggle for the installed controller exit flow, not the course\'s old Y=STOP rule. There is no B button. Servo begin() can move during INIT. runAction() adds queued actions in this SDK. A robot source edit usually needs only a robot upload. Short lesson snippets can omit behavior described in their titles.')
p('Prepared for Galaxy Gladiators, team 185. This guide adds practical explanations and clearly separates trial settings from measured results. It does not claim to resolve the outstanding controller START issue or to validate mechanical travel.','SmallX')

class NumberedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs): super().__init__(*args,**kwargs); self.saved=[]
    def showPage(self): self.saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self.saved)
        for state in self.saved:
            self.__dict__.update(state)
            self.setStrokeColor(TEAL); self.setLineWidth(.7); self.line(46,H-35,W-46,H-35)
            self.setFont('Helvetica',8); self.setFillColor(GRAY)
            self.drawString(46,H-26,'NRL / PROGRAMMING ESSENTIALS')
            self.drawString(46,27,'Galaxy Gladiators  |  16 October 2026')
            self.drawRightString(W-46,27,f'{self._pageNumber} / {total}')
            super().showPage()
        super().save()

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=51,bottomMargin=48,
    title='NRL Programming - Important Notes',author='Galaxy Gladiators study guide',subject='28-module programming curriculum summary')
doc.build(story,canvasmaker=NumberedCanvas)
print(OUT)
