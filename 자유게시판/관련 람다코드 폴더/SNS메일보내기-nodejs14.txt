var AWS = require("aws-sdk");
//var moment = require("moment"); <----moment 패키지를 사용하려면 Layer에 추가해야하기에 주석처리함
//require('moment-timezone'); 
//moment.tz.setDefault("Asia/Seoul"); 

exports.handler = function(event, context) {
	console.log("event: ", event);
	console.log("event type: ", typeof(event))
//	console.log("JSON.parse(event.responsePayload): ", JSON.parse(event.responsePayload))  <--오류 실패 
	
//	var inputjson = JSON.stringify(event)
	console.log("inputjson type: ", typeof(inputjson))
	
	console.log('event["responsePayload"]["age"]: ', event["responsePayload"]["age"]);
	console.log('event["responsePayload"]["product"]: ', event["responsePayload"]["product"]);
	console.log('event["responsePayload"]["customerID"]: ', event["responsePayload"]["customerID"]);
	

	console.log("input json parse complete")
	
	
	//현재 시간
//	var currdate = moment().format('YYYY-MM-DD HH:mm:ss');
//	currdate = currdate + "\n\n";
	
	
	var SNSarnAdd = "arn:aws:sns:us-east-1:569934397842:test-sns";
	
	var subject = "SNS 테스트 test";
	var message = "\n\n";
	message += " 2021-05-03\n\n 람다를 통한 이메일 서비스는 AWS SNS 대신\n\n AWS Lambda + AWS SES (Simple Email Service) 콤보로 접근을 시도할 것\n\n ";
//	message += currdate;
	message = message + event["responsePayload"]["age"] + "\n"
	message = message + event["responsePayload"]["product"] + "\n";
	message = message + event["responsePayload"]["customerID"] + "\n";
	
	
	
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
