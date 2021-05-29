var AWS = require("aws-sdk");
//var moment = require("moment"); <----moment 패키지를 사용하려면 Layer에 추가해야하기에 주석처리
//require('moment-timezone'); 
//moment.tz.setDefault("Asia/Seoul"); 

exports.handler = function(event, context) {
	console.log("event: ", event);
	console.log("event type: ", typeof(event))

	console.log("inputjson type: ", typeof(inputjson))
	console.log('event["responsePayload"]["bucket"]: ', event["responsePayload"]["bucket"]);
	console.log('event["responsePayload"]["file_name"]: ', event["responsePayload"]["file_name"]);
	console.log('event["responsePayload"]["u_bucket"]: ', event["responsePayload"]["u_bucket"]);	
	console.log('event["responsePayload"]["age"]: ', event["responsePayload"]["age"]);
	console.log('event["responsePayload"]["product"]: ', event["responsePayload"]["product"]);
	console.log('event["responsePayload"]["customerID"]: ', event["responsePayload"]["customerID"]);
	console.log('event["responsePayload"]["event_name"]: ', event["responsePayload"]["event_name"]);	
	console.log('event["responsePayload"]["timestamp"]: ', event["responsePayload"]["timestamp"]);	

	console.log("input json parse complete")
	
	
	//현재 시간
//	var currdate = moment().format('YYYY-MM-DD HH:mm:ss');
//	currdate = currdate + "\n\n";
	
	
	var SNSarnAdd = "arn:aws:sns:us-east-1:569934397842:test-sns-to-cbs";
	var subject = "SNS 테스트 test";
	var message = "\n\n";
	
//	message += "Date : " + " 5월 22일 " + "\n\n"
	message += event["responsePayload"]["timestamp"] + " 5월 22일 " + "\n\n"
	message = message + " ★ 안녕하세요! 이벤트샵 알림 service 입니다! ★" + "\n\n"
	message = message + "S3에 Trigger가 발생하였습니다." + "\n" + " ----------------- Trigger 내용은 다음과 같습니다." + "------------------" + "\n"
	message = message + "1. Trigger : " + event["responsePayload"]["event_name"] +"\n"
	message = message + "2. Bucket : " + event["responsePayload"]["bucket"] +"\n"
	message = message + "3. file_name : " + event["responsePayload"]["file_name"] + "\n"
	message = message + event["responsePayload"]["u_bucket"] + " bucket에 파일을 저장하였습니다." +"\n"
	message = message + " --------------  파일 내용" + "  -----------------" + "\n" + "age : " + event["responsePayload"]["age"] + "\n"
	message = message + "product : " + event["responsePayload"]["product"] + "\n"
	message = message + "customerID : " + event["responsePayload"]["customerID"] + "\n" ;

	
	//이메일 발송 내용 로그에 출력
	console.log("Sent Message: " + message)
	
	var sns = new AWS.SNS();
	var params = {
		
		Subject: subject,
		Message: message,
		TopicArn: SNSarnAdd
	};
	sns.publish(params, context.done);
	

};

