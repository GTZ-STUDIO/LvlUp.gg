import React from 'react'
import '../../App.css'
import ExplorePage from '../ExplorePage'
import Cards from '../Cards'
import SearchBar from '../SearchBar'

function Explore () {
    return (
        <>
            <ExplorePage />
            <Cards />
            <SearchBar />
        </>
    )   
}

export default Explore;