import React, { useState, useEffect } from 'react';
import '../App.css';
import { useHistory } from "react-router-dom";
import axios from 'axios';

const RecommendedGuides = () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL;

    const [recommendedGuides, setRecommendedGuides] = useState([]);
    const history = useHistory();

    const gameImageMap = {
        EldenRing: 'images/eldenRing.png',
        Dota2: 'images/dota.jpg',
        LeagueOfLegends: 'images/league.png',
        BaldursGate3: 'images/baldursGate.png',
        CSGO: 'images/csgo.jpg',
    };

    const handleBlogClick = (blogId) => {
        history.push(`/blog/${blogId}`);
    };
    useEffect(() => {
        const fetchRecommendedGuides = async () => {
            try {
                const response = await axios.get(`${backendUrl}/blog/recommended/`);
                setRecommendedGuides(response.data.blogs);
            } catch (error) {
                console.error('Error fetching recommended guides:', error);
            }
        };

        fetchRecommendedGuides();
    }, [backendUrl]);

    return (
        <div style={{position: 'relative', marginLeft: '23.5vw'} }>  
            <ul className='guide-list'>
                {recommendedGuides.slice(0, 5).map((blog) => (
                    <div className='guide-item' key={blog.id} onClick={() => handleBlogClick(blog.id)}>
                        <img src={gameImageMap[blog.game] || 'images/img-home.jpg'} alt={blog.title} className="guide-image" />
                        <div className='guide-title'>{blog.title}</div>
                    </div>
                ))}
            </ul>
        </div>
    );
};

export default RecommendedGuides;
