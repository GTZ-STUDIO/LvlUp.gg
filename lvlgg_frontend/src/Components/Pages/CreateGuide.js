//import React, {useContext, useState} from 'react';
import '../../App.css';
//import { Link, useHistory } from "react-router-dom";
//import axios from "axios";
//import { AuthContext } from '../../Contexts/AuthContext';


export default function CreateGuide() {
  return (
    <form className='createguide'>
      <input type="text" id="title" name="title" placeholder={'Title'}/>
      <textarea name="" id="" cols="30" rows="30" placeholder={'Enter post'}></textarea>
      <button>Post Guide</button>
    </form>
  )
}