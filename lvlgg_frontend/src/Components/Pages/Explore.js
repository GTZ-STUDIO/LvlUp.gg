import React from 'react'
import '../../App.css'
import ExplorePage from '../ExplorePage'
import Cards from '../Cards'
import SearchBar from '../SearchBar'

function Explore () {
    return (
        <>
            <ExplorePage />
            <h1>View our games</h1>
            <h1>Recommened to you</h1>
            <Cards />
            <SearchBar />
        </>
    )   
}

export default Explore;