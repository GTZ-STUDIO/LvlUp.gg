import React from 'react';
import { Link } from 'react-router-dom';

function CardItem({ src, text, gameName }) {
    const handleClick = () => {
      if (gameName) {
        window.location.href = `/guides?gameName=${gameName}`;
      } else {
        window.location.href = '/guides';
      }
    };
  
    return (
      <li className='cards__item' onClick={handleClick}>
        <Link className='cards__item__link' to='/guides'>
          <figure className='cards__item__pic-wrap'>
            <img src={src} alt='Games' className='cards__item__img' />
          </figure>
          <div className='cards__item__info'>
            <h5 className='cards__item__text'>{text}</h5>
          </div>
          <img src='images/up-arrow.png' alt='Arrow Icon' className='cards__item__arrow' />
        </Link>
      </li>
    );
  }
  
  export default CardItem;
  
