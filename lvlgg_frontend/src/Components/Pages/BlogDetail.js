import React, { useEffect, useState, useContext, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { AuthContext } from '../../Contexts/AuthContext'
import axios from 'axios';
import '../../App.css';

const BlogDetail = () => {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const history = useHistory();
  const { userPk } = useContext(AuthContext);
  const { isSignedIn } = useContext(AuthContext);
  const [likes, setLikes] = useState(blog?.likes || 0);
  const [dislikes, setDislikes] = useState(blog?.dislikes || 0);
  const [isLiked, setIsLiked] = useState(false);
  const [isDisliked, setIsDisliked] = useState(false);


  const gameImageMap = {
    "EldenRing": "url(/images/eldenRing.png)",
    "LeagueOfLegends": "url(/images/league.png)",
    "Dota2": "url(/images/dota.jpg)",
    "CSGO": "url(/images/csgo.jpg)",
    "BaldursGate3": "url(/images/baldursGate.jpeg)",
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
    axios.put(`http://localhost:8000/blog/likes/${id}/`, { action: 'like', value: 1 },{
      headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    withCredentials: true,})
      .then(response => {
        setLikes(response.data.likes);
        alert('Guide Liked')
        setIsLiked(true);
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
    axios.put(`http://localhost:8000/blog/likes/${id}/`, { action: 'dislike', value: 1 },{
      headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    withCredentials: true,}
    )
      .then(response => {
        setDislikes(response.data.dislikes);
        alert('Guide Disiked')
        setIsDisliked(true);
      })
      .catch(error => {
        console.error('Error disliking blog:', error);
      });
  };

  const fetchComments = useCallback(() => {
    axios.get(`http://localhost:8000/comment/get_comments/${id}/`)
      .then(response => {
        setComments(response.data.comments);
      })
      .catch(error => {
        console.error('Error fetching comments:', error);
      });
  }, [id]);

  useEffect(() => {
    if (isNaN(id)) {
      history.push("/about");
      return;
    }
    axios.get(`http://localhost:8000/blog/get_blog/?id=${id}`)
      .then(response => {
        setBlog(response.data.blogs[0]);
        fetchComments();
      })
      .catch(error => {
        console.error('Error fetching blog:', error);
      });
  }, [id, history, fetchComments]);

  const handleCommentSubmit = (e) => {
    const csrfToken = getCookie('csrftoken');
    e.preventDefault();
  
    axios.post('http://localhost:8000/comment/create_comment/', {
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
  
  return (
    <div className="page-container" style={{ backgroundImage: gameImageMap[blog?.game] }}>
      <div className="overlay" style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)', 
      }}></div>
      <div className="blog-detail-container">
        <h1 className="blog-title">{blog?.title}</h1>
        <p className="blog-content">{blog?.content}</p>
        <p className="blog-metadata">Date Posted: {blog?.date_posted}</p>
        <p className="blog-metadata">Author: {blog?.author}</p>
        <p className="blog-metadata">Likes: {blog?.likes}</p>
        <p className="blog-metadata">Dislikes: {blog?.dislikes}</p>

        <div className="like-dislike-buttons">
          <button onClick={handleLike}>Like</button>
          <button onClick={handleDislike}>Dislike</button>
        </div>
        
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
