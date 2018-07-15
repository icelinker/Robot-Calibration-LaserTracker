MODULE COMM_ABB2PYTHON
! This code puts the ABB starts the controller in server mode and wait connection
! from client.After the connection has been established, it waits commands from
! MATLAB.

VAR socketdev server_socket;
VAR socketdev client_socket;
VAR string ServerIPAddress:= "192.168.125.1";
VAR num ServerPort:= 1025;
VAR string client_ip;
VAR speeddata vCustom:=[250,500,9E9,9E9];

!CONST string terminator := "\0A";

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: main loop acting as a listening server
!@param: none
!**************************************************************************************************

PROC main()
    VAR byte actioncode := 0;

	TPErase;
	
	!Init TCP connection
	COMM_TCPInit;
    
	WHILE TRUE DO
        
		!Waiting for the client (MATLAB) to send some information
        actioncode := COMM_GetActionCode();
		
        !**************************  Add new actions here  ********************
        !**************************      ||       ||       ********************
        !**************************      \/       \/       ********************
        
        !list of commands that can only be executed if the robot is not moving   
		TEST actioncode
			CASE 1:	COMM_SendJoints;
			CASE 2:	COMM_MoveAbsJ;
            CASE 3:	COMM_SetTCPSpeed;
            CASE 4:	COMM_MoveAbsJNowait;
		ENDTEST
        !list of commands that can be executed even if the robot is moving
      

        !**********************************************************************
        !****************************** End of actions ************************
        !**********************************************************************
	ENDWHILE										
ENDPROC

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 29/01/2015
!@desc: 
!@param: none
!@return true if robot is in position
!**************************************************************************************************
LOCAL FUNC bool isRobotAtPosition(VAR jointtarget joints)
    VAR jointtarget currentjoints;
    VAR num tolerance;
    tolerance := 0.01;
    currentjoints := CJointT();
    IF abs(joints.robax.rax_1 - currentjoints.robax.rax_1) < tolerance AND
        abs(joints.robax.rax_2 - currentjoints.robax.rax_2) < tolerance AND
        abs(joints.robax.rax_3 - currentjoints.robax.rax_3) < tolerance AND
        abs(joints.robax.rax_4 - currentjoints.robax.rax_4) < tolerance AND
        abs(joints.robax.rax_5 - currentjoints.robax.rax_5) < tolerance AND
        abs(joints.robax.rax_6 - currentjoints.robax.rax_6) < tolerance THEN
        RETURN TRUE;
    ENDIF
    RETURN FALSE;
ENDFUNC
!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: Set the linear TCP speed of the robot to the value (mm/s) sent by the client (MATLAB)
!@param: none
!**************************************************************************************************
LOCAL PROC COMM_SetTCPSpeed()
    VAR rawbytes receive_message;
    
    !receive the data from MATLAB
	SocketReceive client_socket \RawData := receive_message \ReadNoOfBytes := 4 \Time:= WAIT_MAX;
    
    !unpack speeddata 
    UnpackRawBytes receive_message, \Network, 1, vCustom.v_tcp \IntX := DINT;
    
    TPWrite "Speed changed to: " \Num:=vCustom.v_tcp;
    
ENDPROC
!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: Move the robot to the joint values sent by the client (MATLAB)
!@param: none
!**************************************************************************************************
LOCAL PROC COMM_MoveAbsJ()
	VAR rawbytes receive_message;
	VAR jointtarget joints;
	VAR byte send_message{1} := [1];
    
    !receive the data from MATLAB
	SocketReceive client_socket \RawData := receive_message \ReadNoOfBytes := 24 \Time:= WAIT_MAX;
    
    !store all 6 joints in jointtarget
	UnpackRawBytes receive_message, \Network, 1, joints.robax.rax_1 \float4;
	UnpackRawBytes receive_message, \Network, 5, joints.robax.rax_2 \float4;
	UnpackRawBytes receive_message, \Network, 9, joints.robax.rax_3 \float4;
	UnpackRawBytes receive_message, \Network, 13, joints.robax.rax_4 \float4;
	UnpackRawBytes receive_message, \Network, 17, joints.robax.rax_5 \float4;
	UnpackRawBytes receive_message, \Network, 21, joints.robax.rax_6 \float4;
    
    !move the robot to the desired joints values
	MoveAbsJ joints, vCustom, fine, tool0;
    
    !send 1 to the client to confirm the movement have been completed
	SocketSend client_socket \Data := send_message;
ENDPROC

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: Move the robot to the joint values sent by the client (MATLAB)
!@param: none
!**************************************************************************************************
LOCAL PROC COMM_MoveAbsJNoWait()
	VAR rawbytes receive_message;
	VAR jointtarget joints;
    VAR jointtarget currentjoints;
	VAR byte send_message{1} := [1];

    
    !receive the data from MATLAB
	SocketReceive client_socket \RawData := receive_message \ReadNoOfBytes := 24 \Time:= WAIT_MAX;
    
    !store all 6 joints in jointtarget
	UnpackRawBytes receive_message, \Network, 1, joints.robax.rax_1 \float4;
	UnpackRawBytes receive_message, \Network, 5, joints.robax.rax_2 \float4;
	UnpackRawBytes receive_message, \Network, 9, joints.robax.rax_3 \float4;
	UnpackRawBytes receive_message, \Network, 13, joints.robax.rax_4 \float4;
	UnpackRawBytes receive_message, \Network, 17, joints.robax.rax_5 \float4;
	UnpackRawBytes receive_message, \Network, 21, joints.robax.rax_6 \float4;
    
    !move the robot to the desired joints values
	MoveAbsJ \Conc, joints, vCustom, fine, tool0;

ENDPROC

    

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: Send actual joint values to the client (MATLAB) 
!@param: none
!**************************************************************************************************
LOCAL PROC COMM_SendJoints()
	VAR rawbytes send_message;
	VAR jointtarget joints;
    
    !get the current joint values on the robot
	joints := CJointT();
    
    !convert the joints values in rawbytes to send to the client (MATLAB)
	PackRawBytes joints.robax.rax_1, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in degrees
	PackRawBytes joints.robax.rax_2, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in degrees
	PackRawBytes joints.robax.rax_3, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in degrees
	PackRawBytes joints.robax.rax_4, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in degrees
	PackRawBytes joints.robax.rax_5, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in radians
	PackRawBytes joints.robax.rax_6, send_message, \Network, (RawBytesLen(send_message)+1), \Float4; !Send the joint angle in radians
	
	!Send the joint angles to client
	SocketSend client_socket \RawData := send_message;
    
	ERROR
		IF ERRNO=ERR_SOCK_TIMEOUT THEN
			RETRY;
		ENDIF
ENDPROC

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: This function creates the connection between the server (controller) and the client (MATLAB)
!@param: none
!**************************************************************************************************
LOCAL PROC COMM_Connect2Client()
	VAR string client_ip := "";
    
	WHILE strlen(client_ip) = 0 DO
		SocketAccept server_socket, client_socket, \ClientAddress:=client_ip;
	ENDWHILE
	TPWrite "Client at " + client_ip + " connected.";
	ERROR
		IF ERRNO=ERR_SOCK_TIMEOUT THEN
			TRYNEXT;
		ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
			COMM_TCPInit;
			RETRY;
		ENDIF
        
ENDPROC

!**************************************************************************************************
! @author: Martin Gaudreault
! @date of creation: 26/01/2015
! @desc: Initialise the TCP connection on the controller (acting as a server).
! @param: none
!**************************************************************************************************
LOCAL PROC COMM_TCPInit()
	VAR string client_ip;
    
	SocketCreate server_socket;
	SocketBind server_socket, ServerIPAddress, ServerPort;
	SocketListen server_socket;
	TPWrite "Server socket initialised. Waiting for client connection.";
	COMM_Connect2Client;
	ERROR
		IF ERRNO=ERR_SOCK_CLOSED THEN
			TRYNEXT;
		ELSEIF ERRNO=ERR_SOCK_TIMEOUT THEN
			RETRY;
		ENDIF
ENDPROC

!**************************************************************************************************
!@author: Martin Gaudreault
!@date of creation: 26/01/2015
!@desc: Receive the action code sent from the client and returns it as a byte.
!@param: none
!@return byte - the action code
!**************************************************************************************************
LOCAL FUNC byte COMM_GetActionCode()
    	VAR rawbytes receive_message;
    	VAR byte actioncode := 0;
        
        !receive the byte of the required action code
		SocketReceive client_socket \RawData := receive_message \ReadNoOfBytes := 1 \Time:= WAIT_MAX;
        
        !store it into value
		UnpackRawBytes receive_message, \Network, 1, actioncode \Hex1;
        TPWrite "Received message is: " \Num:=actioncode;
        
        RETURN actioncode;
ERROR 
	IF ERRNO=ERR_SOCK_TIMEOUT THEN
		RETRY;
	ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
		TPWrite "Client disconnected";
		EXIT;
	ELSE
		! No error recovery handling
	ENDIF
UNDO
	SocketClose server_socket;
	SocketClose client_socket;	
ENDFUNC

ENDMODULE