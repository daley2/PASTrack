import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { logout, me } from '../lib/auth.js'

function NavItem({ to, label }) {
    return (
        <NavLink
            to={to}
            className={({ isActive }) =>
                `rounded px-3 py-2 text-sm ${isActive ? 'bg-slate-200 text-slate-900' : 'text-slate-700 hover:bg-slate-100'}`
            }
        >
            {label}
        </NavLink>
    )
}

export default function Shell() {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const navigate = useNavigate()

    useEffect(() => {
        me()
            .then(setUser)
            .catch(() => setUser(null))
            .finally(() => setLoading(false))
    }, [])

    async function onLogout() {
        try {
            await logout()
        } finally {
            navigate('/login')
        }
    }

    if (loading) return <div className="p-6">Loading…</div>
    if (!user) {
        navigate('/login')
        return null
    }

    return (
        <div className="min-h-screen">
            <header className="border-b border-slate-200 bg-white">
                <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
                    <Link to="/dashboard" className="text-sm font-semibold text-slate-900">
                        PAStrack
                    </Link>
                    <nav className="flex items-center gap-1">
                        <NavItem to="/dashboard" label="Dashboard" />
                        <NavItem to="/submissions" label="Submissions" />
                        <NavItem to="/submit" label="New Request" />
                        <NavItem to="/profile" label="Profile" />
                    </nav>
                    <div className="flex items-center gap-3">
                        <div className="text-right">
                            <div className="text-xs font-medium text-slate-900">{user.full_name || user.email}</div>
                            <div className="text-xs text-slate-600">{user.role_label}</div>
                        </div>
                        <button onClick={onLogout} className="rounded px-3 py-2 text-sm text-slate-700 hover:bg-slate-100">
                            Logout
                        </button>
                    </div>
                </div>
            </header>
            <main className="mx-auto max-w-6xl px-4 py-6">
                <Outlet />
            </main>
        </div>
    )
}
