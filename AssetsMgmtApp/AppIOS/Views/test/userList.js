/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TabBarIOS,
  NavigatorIOS,
  AlertIOS,
  ActivityIndicatorIOS
} from 'react-native';

var Api = require('../../Network/NetworkAPI');

class userList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      selectedTab: "home",
    };
  }
  componentDidMount() {
    this.fetchData();
  }
  fetchData() {
    console.log(Api.getUser());
    fetch(Api.getUser())
    .then((response) => response.json())
    .then((responseData) => {
        console.log(responseData);
        this.setState({
          loaded: true,
          data:responseData.col1,
          presses: 0,
          notifCount: 0,
        });
    })
    .catch((error) => {
        console.warn(error);
    })
    .done();
  }
  renderLoading() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>
          Loading data.......
        </Text>
      </View>
    );
  }

  renderData(data) {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>
          User Information:
        </Text>
        <Text style={styles.instructions}>
          Name: {data.name} 
        </Text>
        <Text style={styles.instructions}>
          Full Name: {data.full_name} 
        </Text>
        <Text style={styles.instructions}>
          Email: {data.email} 
        </Text>
        <Text style={styles.instructions}>
          Add Time: {data.add_time} 
        </Text>
      </View>
    );
  }

  render() {

    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>
          here test
        </Text>
      </View>
    );

    if(!this.state.loaded)
    {
        return this.renderLoading();
    }

    var data = this.state.data;
    return this.renderData(data);
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    fontSize: 15,
    textAlign: 'left',
    color: '#333333',
    marginBottom: 5,
  },
});

module.exports = userList;
