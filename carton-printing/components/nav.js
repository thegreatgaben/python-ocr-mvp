import React from 'react'
import Link from 'next/link'
import style from './nav.scss';

const Nav = () => (
  <nav className={style.nav}>
    <ul>
      <li>
        <Link href='../pages/login'>
          <a>Login</a>
        </Link>
      </li>

    </ul>
  </nav>
)

export default Nav
