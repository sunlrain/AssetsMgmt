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
var _url='http://www.csdn.com';

class Web extends Component{
  constructor(props) {
    super(props);
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
            source={{uri:_url}}
            automatioallyAdjustContentInsets={false}
            startInLoadingStatus={true}
            scalesPageToFit={true}
          />
      </View>

    );
  }
}

class About extends Component {
  constructor(props) {
    super(props);
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

              <TouchableOpacity onPress={() => _navigator.push({title:'Kevin', id:'http'})}>
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