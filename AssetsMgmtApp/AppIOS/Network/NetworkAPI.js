'use strict';
var BASE = 'http://106.187.46.80:5002/';
var ACCESS_TOKEN = '495c7bef0f438c5505ebdecabd4fce87ac7764f79ccaed608412f3199041d66d';

function api(api, v){
	if(v instanceof Object){
		var p = Object.keys(v).map(function(k) {
			return encodeURIComponent(k) + "=" + encodeURIComponent(v[k]);
		}).join('&');
	}else{
		var p = v;
	}
	return BASE + api + '?access_token=' + ACCESS_TOKEN + '&' + p;
}

function addUser(){
	return api('add_user');
}

function getUser(){
	return api('get_user');
}

// function getHomeTopics(offset, limit){
// 	return api('topics.json', {'type':'excellent','offset':offset, 'limit':limit});
// }

// function getNodeTopics(node_id, offset, limit){
// 	return api('topics.json', {'node_id':node_id, 'offset':offset, 'limit':limit});
// }

// function getTopic(id){
// 	return api('topics/'+id+'.json');
// }

module.exports = {
	AddUser: addUser,
	getUser: getUser
};