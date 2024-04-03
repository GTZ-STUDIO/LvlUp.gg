import React, { useEffect, useState, useContext, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { AuthContext } from '../../Contexts/AuthContext'
import axios from 'axios';
import '../../App.css';

const BlogDetail = () => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const history = useHistory();
  const { userPk } = useContext(AuthContext);
  const { isSignedIn } = useContext(AuthContext);
  const [isLiked, setIsLiked] = useState(false);
  const [isDisliked, setIsDisliked] = useState(false);
  const [isFavorited, setIsFavorited] = useState(false);


  const gameImageMap = {
    "EldenRing": "url(/images/eldenRing.png)",
    "LeagueOfLegends": "url(/images/league.png)",
    "Dota2": "url(/images/dota.jpg)",
    "CSGO": "url(/images/csgo.jpg)",
    "BaldursGate3": "url(/images/baldursGate.png)",
  };

  const getCookie = (name) => {
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith(`${name}=`));
    if (cookieValue) {
      return cookieValue.split('=')[1];
    }
    return null;
  };

  const handleLike = () => {
    if(isLiked){
      return;
    } 
    const csrfToken = getCookie('csrftoken');
    axios.put(`${backendUrl}/blog/likes/${id}/`, { action: 'like', value: 1 },{
      headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    withCredentials: true,})
      .then(response => {
        setBlog(prevBlog => ({
          ...prevBlog,
          likes: response.data.likes,
        }));
        setIsLiked(true);
        alert('Guide Liked')
      })
      .catch(error => {
        console.error('Error liking blog:', error);
      });
  };

  const handleDislike = () => {
    if (isDisliked) {
      return; 
    }
    const csrfToken = getCookie('csrftoken');
    axios.put(`${backendUrl}/blog/likes/${id}/`, { action: 'dislike', value: 1 },{
      headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    withCredentials: true,}
    )
      .then(response => {
        setBlog(prevBlog => ({
        ...prevBlog,
        dislikes: response.data.dislikes,
      }));
      setIsDisliked(true);
        alert('Guide Disiked')
        
      })
      .catch(error => {
        console.error('Error disliking blog:', error);
      });
  };

  const handleFavorite = () => {
    const csrfToken = getCookie('csrftoken');
    const action = isFavorited ? 'unsubscribe' : 'subscribe';
    const method = isFavorited ? 'DELETE' : 'POST';  
    axios.request({
      url: `${backendUrl}/favourite/${action}/${id}/`,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      withCredentials: true,
    })
    .then(response => {
      setIsFavorited(!isFavorited);
      localStorage.setItem(`favorited-${id}`, !isFavorited);
      alert(`Guide ${isFavorited ? 'Unfavorited' : 'Favorited'}`);
    })
    .catch(error => {
      console.error(`Error ${isFavorited ? 'unfavoriting' : 'favoriting'} blog:`, error);
    });
  };

  const fetchComments = useCallback(() => {
    axios.get(`${backendUrl}/comment/get_comments/${id}/`)
      .then(response => {
        setComments(response.data.comments);
      })
      .catch(error => {
        console.error('Error fetching comments:', error);
      });
  }, [id, backendUrl]);

  const handleCommentSubmit = (e) => {
    const csrfToken = getCookie('csrftoken');
    e.preventDefault();
  
    axios.post(`${backendUrl}/comment/create_comment/`, {
      content: newComment,
      author: userPk, 
      blog: id,
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      withCredentials: true,
    })
    .then(response => {
      if (response.status === 200) {
        setNewComment('');
        fetchComments();
        console.log('Comment submitted successfully');
        alert('Comment Successfully Created')
      } else {
        console.error('Error submitting comment:', response.statusText);
      }
    })
    .catch(error => {
      console.error('Error submitting comment:', error);
    });
  };  

  useEffect(() => {
    if (isNaN(id)) {
      history.push("/about");
      return;
    }
    axios.get(`${backendUrl}/blog/get_blog/?id=${id}`)
      .then(response => {
        setBlog(response.data.blogs[0]);
        
        const isFavoritedLocal = localStorage.getItem(`favorited-${id}`);
        setIsFavorited(isFavoritedLocal === 'true');
      
        fetchComments();
      })
      .catch(error => {
        console.error('Error fetching blog:', error);
      });
  }, [id, history, backendUrl, fetchComments]);
  
  return (
    <div className="page-container" style={{ backgroundImage: gameImageMap[blog?.game]}}>
      <div className="blog-detail-container">
        <h1 className="blog-title">{blog?.title}</h1>
        <p className="blog-content">{blog?.content}</p>
        <div className="blog-metadata">
          <p>Date Posted: {blog?.date_posted}</p>
          <p>Author: {blog?.author}</p>
          <p>Likes: {blog?.likes}</p>
          <p>Dislikes: {blog?.dislikes}</p>
        </div>
        {isSignedIn && (
          <div>
            <div className="like-dislike-buttons">
              <button onClick={handleLike}>Like</button>
              <button onClick={handleDislike}>Dislike</button>
              <button onClick={handleFavorite} className="favorite-button">
                {isFavorited ? 'Unfavorite' : 'Favorite'}
              </button>
            </div>
          </div>
        )}
        <h2>Comments</h2>
        <div className="comments-container">
          {comments.map(comment => (
            <div key={comment.id} className="comment">
              <p>{comment.content}</p>
              <p>Posted by: {comment.username}</p>
            </div>
          ))}
        </div>
        {isSignedIn ? (
          <form onSubmit={handleCommentSubmit}>
            <textarea className='comment-textarea'
              placeholder="Write a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              required
            ></textarea>
            <button type="submit" className='comment-button'>Submit</button>
          </form>
        ) : (
          <p>Please sign in to leave a comment</p>
        )}
      </div>
    </div>
  );
};

export default BlogDetail;
