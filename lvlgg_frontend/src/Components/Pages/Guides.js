import React, {useContext, useState} from 'react';
import '../../App.css';
import { Link, useHistory } from "react-router-dom";
import axios from "axios";
import { AuthContext } from '../../Contexts/AuthContext'


export default function Guides() {
  const {setIsSignedIn} = useContext(AuthContext);
  return (
    <div className='guides'>
      <Link to='/createguide'>
        <button className='guides-button'>Create Guide</button>
      </Link>
    </div>
  )
}