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
  const [user, setUser] = useState("");

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

  const fetchComments = useCallback(() => {
    axios.get(`http://localhost:8000/comment/get_comments/${id}/`)
      .then(response => {
        setComments(response.data.comments);
      })
      .catch(error => {
        console.error('Error fetching comments:', error);
      });
  }, [id]);

  const handleUsername = useCallback(() => {
    axios
      .get(`http://localhost:8000/account/${userPk}/`, {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        withCredentials: true,
      })
      .then((response) => {
        if (response.status === 200) {
          console.log("got Username successfully");
          setUser(response.data.username);
        } else {
          console.log("Username change unsuccessful");
        }
      })
      .catch((error) => {
        console.error("Error updating username:", error);
      });
  }, [userPk]);

  useEffect(() => {
    handleUsername();
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
  }, [id, history, fetchComments, handleUsername]);

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
      <div className="blog-detail-container">
        <h1 className="blog-title">{blog?.title}</h1>
        <p className="blog-content">{blog?.content}</p>
        <p className="blog-metadata">Date Posted: {blog?.date_posted}</p>
        <p className="blog-metadata">Author: {blog?.author}</p>
        
        <h2>Comments</h2>
        <div className="comments-container">
          {comments.map(comment => (
            <div key={comment.id} className="comment">
              <p>{comment.content}</p>
              <p>Posted by: {comment.author}</p>
            </div>
          ))}
        </div>
  
        {isSignedIn ? (
          <form onSubmit={handleCommentSubmit}>
            <textarea
              placeholder="Write a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              required
            ></textarea>
            <button type="submit">Submit</button>
          </form>
        ) : (
          <p>Please sign in to leave a comment</p>
        )}
      </div>
    </div>
  );
};

export default BlogDetail;
