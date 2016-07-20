import React, { Component } from 'react';
import {
  StyleSheet,
  View,
  Image,
  Text,
  WebView,
  Navigator,
  TouchableOpacity,
} from 'react-native';

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10
  },
  ad: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'left'
  },
  link: {
    marginTop: 20,
    color: '#356DD0',
  },
  logo: {
    height: 150,
    width: 150,
  }
});

var _url='http://www.csdn.com';

class Web extends Component{
  // constructor(props) {
  //   super(props);
  // }
  render() {
    const { navigator } = this.props;
    return (
      <View style={{flex:1}}>
          <TouchableOpacity onPress={() => navigator.pop()}>
            <Text style={styles.link}>
              Back
            </Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => navigator.push({title:'Kevin', id:'http'})}>
            <Text style={styles.link}>
              Forward
            </Text>
          </TouchableOpacity>
          <WebView 
            source={{uri:_url}}
            automatioallyAdjustContentInsets={false}
            startInLoadingStatus={true}
            scalesPageToFit={true}
          />
      </View>

    );
  }
}