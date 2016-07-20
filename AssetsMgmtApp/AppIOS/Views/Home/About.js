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

var logo=require('../../Resources/ubuntu.png');
var _navigator;

import Web from './Web'

class About extends Component {
  constructor(props) {
    super(props);
    const { navigator } = this.props; 
    if (navigator)
       console.log("Navigator is not null")
    // this.state = {
    //   navigator: this.props.navigator,
    // };
  }

  renderScene (route, navigator)
  {
    _navigator = navigator;

    if(route.id === 'main')
    {
        return (
          <View style={styles.container}>
              <Image style={styles.logo} source={logo} />
              <Text style={styles.ad}>
                Yes, you are right!
              </Text>
              <Text style={styles.ad}>
                This is the Tools for Management.
              </Text>

              <TouchableOpacity onPress={() => _navigator.push({title:'Kevin2', id:'http2'})}>
                <Text style={styles.link}>
                  http://www.csdn.com
                </Text>
              </TouchableOpacity>
          </View>
        );
    }

    if (route.id === 'http')
    {
      return (
          <Web navigator={navigator} route={route} />
        );
    }
    if (route.id === 'http2')
    {
      return (
          <Web navigator={navigator} route={route} />
        );
    }
  }

  render() {
    var renderScene = this.renderScene;
    return (
        <Navigator 
          initialRoute={{title:'Main', id:'main'}}
          renderScene={renderScene}
        />
      );
  }

}

module.exports = About;