/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  Text,
  View,
  TouchableHighlight,
} from 'react-native';

var styles = require('./UserCellStyleSheet');
var Api = require('../../Network/NetworkAPI');

class UserCell extends Component {

  render() {

    var data = this.props.data;
    return (
      <TouchableHighlight onPress={this.props.onSelect} underlayColor={'#eeeeee'}>
        <View style={Style.container}>
          <View style={Style.topic}>
            <Text style={Style.title}>
              {data.title}
            </Text>
            {this.renderInfo()}
          </View>

          {this.renderCommentCount()}
        </View>
      </TouchableHighlight>
    );
  }

  renderCommentCount(){
    var data = this.props.data;
    if(data.replies_count){
      var comment_width = 20 + data.replies_count.toString().length * 8;
      return (
          <View style={Style.replyNumWrapper}>
            <View style={[Style.replyNum, {width: comment_width}]}>
              <Text style={Style.replyNumText}>{data.replies_count}</Text>
            </View>
          </View>
        );
    }
    return;
  }

  renderInfo(){
    var data = this.props.data;
    if(data.replied_at){
      return (
            <Text style={Style.info}>
              <Text style={Style.node_name}>{data.node_name}</Text> • 
              <Text style={Style.user}>{data.user.login}</Text> • 
              <Text>最后由</Text>
              <Text style={Style.user}>{data.node_name}</Text> 
              <Text style={Style.time}>于发布</Text>
            </Text>
            );
    }
    return (
            <Text style={Style.info}>
              <Text style={Style.node_name}>{data.node_name}</Text> • 
              <Text style={Style.user}>{data.user.login}</Text> • 
              <Text style={Style.time}>于发布</Text>
            </Text>
      );
  }

}

module.exports = UserCell;
