import React from 'react';
import CardItem from './CardItem';
import './Cards.css';

function Cards() {
  return (
    <div className='cards'>
      <div className='cards__container'>
        <div className='cards__wrapper'>
          <h1>View Games</h1>
          <ul className='cards__items'>
            <CardItem
              src='images/eldenRing.png'
              text='Explore Elden Ring Guides'
              gameName='EldenRing'
            />
            <CardItem
              src='images/dota.jpg'
              text='Explore Dota 2 Guides'
              gameName='Dota2'
            />
            <CardItem
              src='images/league.png'
              text='Explore League of Legends Guides'
              gameName='LeagueOfLegends'
            />
            <CardItem
              src='images/baldursgate.png'
              text='Explore Baldurs gate 3 Guides'
              gameName='BaldursGate3'
            />
            <CardItem
              src='images/csgo.jpg'
              text='Explore CSGO Guides'
              gameName='CSGO'
            />
          </ul>
        </div>
      </div>
      <h2>Recommended Games</h2>
    </div>
  );
}

export default Cards;
