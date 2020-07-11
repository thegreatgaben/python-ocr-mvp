import React from 'react';
import Head from 'next/head'
import Nav from '../../components/nav'
import style from './login.scss'

const LoginPage = () => {
  return (
    <div>
      <Head>
        <title>Login</title>
      </Head>

      <Nav/>

      <div className={style.login}>
        <form>
          <div>
            <input type="text" placeholder="username"/>
          </div>
          <div>
            <input type="password" placeholder="password"/>
          </div>
          <button>Submit</button>
        </form>
      </div>
    </div>
  );
}

// LoginPage.getInitialProps = async () => {
//   let response = {}
//   try {
//     response = await axios.get('https://api.tvmaze.com/search/shows?q=batman')
//   } catch (e) {
//     console.log({e})
//   }
//
//   return {
//     data: response
//   }
// }

export default LoginPage
