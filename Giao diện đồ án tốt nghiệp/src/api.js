import {API_URL} from './config/config';

export const authGet = (dispatch, token, url) => {
    return fetch(API_URL + url, {
      method: "GET",
      headers: {
        "content-type": "application/json",
        "X-Auth-Token": token,
      },
    }).then(
      (res) => {
        if (!res.ok) {
          if (res.status === 401) {
            dispatch(failed());
            throw Error("Unauthorized");
          }
          else {
            console.log(res)
            try { res.json().then(res1 => console.log(res1)) }
            catch (err) {}
            throw Error();
          }
          return null;
        }
        return res.json();
      },
      (error) => {
        console.log(error);
      }
    );
};


export const authPost = (dispatch, token, url, body) => {
  return fetch(API_URL + url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "X-Auth-Token": token,
    },
    body: JSON.stringify(body),
  }).then(
    (res) => {
      if (!res.ok) {
        if (res.status === 401) {
          dispatch(failed());
          throw Error("Unauthorized");
        }
        else {
          console.log(res)
          try { res.json().then(res1 => console.log(res1)) }
          catch (err) { }
          throw Error();
        }
        return null;
      }
      return res.json();
    },
    (error) => {
      console.log(error);
    }
  );
};
