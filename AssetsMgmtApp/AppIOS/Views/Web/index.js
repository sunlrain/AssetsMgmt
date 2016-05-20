/*
Coded by: Simar (github.com/iSimar)
GitHub Project: https://github.com/iSimar/HackerNews-React-Native
*/

import React, { Component } from 'react';
import {
  View,
  WebView,
  StyleSheet,
  TouchableOpacity,
  Text,
} from 'react-native';

var styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F6F6EF',
    flexDirection: 'column',
  },
  link: {
    marginTop: 20,
    color: '#356DD0',
  },
});

var _navigator;
var _url;

class Web extends Component{

  constructor(props) {
    super(props);
    _navigator = this.props.navigator;
    _url = this.props._url;
  }

  render() {
    return (
        <View style={{flex:1}}>
          <TouchableOpacity onPress={() => _navigator.pop()}>
            <Text style={styles.link}>
              Back
            </Text>
          </TouchableOpacity>
          <WebView 
            source={{uri:{_url}}}
            automatioallyAdjustContentInsets={false}
            startInLoadingStatus={true}
            scalesPageToFit={true}
          />
      </View>
    );
  }
}

module.exports = Web;