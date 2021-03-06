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
  AlertIOS,
} from 'react-native';

var Api = require('../../Network/NetworkAPI');

class Brief extends Component {
  constructor(props) {
    super(props);
     this.state = {
      data: null,
      loaded: false,
    };
  }

  componentDidMount() {
    this.fetchData();
  }
  fetchData() {
    // console.log(Api.getUser());
    fetch(Api.getSummary())
    .then((response) => response.json())
    .then((responseData) => {
        // console.log(responseData);
        this.setState({
          loaded: true,
          data:responseData.summary,
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
    // console.warn(data.length);
    let items = data;
    return (
      <View style={styles.container}>
      {
        items.map(function (item){
          return (        
            <Text key={item.name} style={styles.welcome}>
              {item.name}:{item.info}
            </Text>
            )
        })
      }
      </View>
    );


  }

  render() {

    // return (
    //   <View style={styles.container}>
    //     <Text style={styles.welcome}>
    //       here test
    //     </Text>
    //   </View>
    // );

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

module.exports = Brief;
