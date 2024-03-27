import React from 'react'
import '../../App.css'
import ExplorePage from '../ExplorePage'
import Cards from '../Cards'
import SearchBar from '../SearchBar'
import RecommendedGuides from '../RecommendedGuides'

function Explore () {
    return (
        <>
            <ExplorePage />
            <SearchBar />
            <Cards />
            <RecommendedGuides/>
        </>
    )   
}

export default Explore;