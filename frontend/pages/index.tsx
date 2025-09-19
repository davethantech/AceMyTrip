import React, { useState, useEffect } from 'react';
import { Search, Bell, Plane, RefreshCw, DollarSign } from 'lucide-react';

// Minimal API client that talks to backend endpoints
class LoyaltyAPI {
  baseURL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') + '/api';

  async request(path, options = {}){
    const res = await fetch(this.baseURL + path, options);
    if (!res.ok) throw new Error('API error: ' + res.status);
    return res.json();
  }

  async getBalances(){ return this.request('/loyalty/balances'); }
  async getRecommendations(){ return this.request('/optimize/recommendations'); }
  async searchWithQuery(q){ return this.request('/optimize/query', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ query: q }) }); }
  async syncAccount(id){ return this.request('/loyalty/sync/' + id, { method: 'POST' }); }
}

const api = new LoyaltyAPI();

const formatPoints = (n:number) => n?.toLocaleString();

export default function Home(){ 
  const [user] = useState({ name: 'Chetan' });
  const [balances, setBalances] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('I want to go to Paris in June for 7 days');
  const [searchResults, setSearchResults] = useState<any|null>(null);
  const [loading, setLoading] = useState({ balances:false, search:false, sync:{} as any });

  useEffect(()=>{ loadInitial(); }, []);

  async function loadInitial(){
    setLoading(s=>({ ...s, balances:true }));
    try{
      const b = await api.getBalances();
      const r = await api.getRecommendations();
      setBalances(b || []);
      setRecommendations(r || []);
    }catch(e){ console.error(e); }
    setLoading(s=>({ ...s, balances:false }));
  }

  async function handleSearch(){
    if(!searchQuery) return;
    setLoading(s=>({ ...s, search:true }));
    try{
      const res = await api.searchWithQuery(searchQuery);
      setSearchResults(res);
    }catch(e){ console.error(e); }
    setLoading(s=>({ ...s, search:false }));
  }

  async function handleSyncAccount(id:string){
    setLoading(s=>({ ...s, sync:{ ...s.sync, [id]: true } }));
    try{
      await api.syncAccount(id);
      await loadInitial();
    }catch(e){ console.error(e); }
    setLoading(s=>({ ...s, sync:{ ...s.sync, [id]: false } }));
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg flex items-center justify-center shadow-md">
                <Plane className="w-6 h-6 text-white transform -rotate-45" />
              </div>
              <span className="text-2xl font-bold text-gray-900">AceMyTravel</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <div className="font-medium text-gray-900">Dashboard</div>
              <div className="text-gray-500 hover:text-gray-700">Search</div>
              <div className="text-gray-500 hover:text-gray-700">Alerts</div>
            </nav>
            <div className="flex items-center space-x-4">
              <Bell className="w-5 h-5 text-gray-500" />
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-semibold">C</span>
                </div>
                <span className="font-medium text-gray-900">{user.name}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome, {user.name}</h1>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Points</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {balances.map(b => (
              <div key={b.account_id} className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center space-x-3 mb-6">
                  <div className={"w-14 h-10 rounded-md flex items-center justify-center " + (b.program_name === 'amex' ? 'bg-blue-600' : b.program_name === 'united' ? 'bg-blue-800' : 'bg-red-700')}>
                    <span className="text-white text-xs font-bold tracking-wide">{b.program_name.toUpperCase()}</span>
                  </div>
                  <span className="font-bold text-lg text-gray-900">{b.program_name.toUpperCase()}</span>
                  <button onClick={()=>handleSyncAccount(b.account_id)} className="ml-auto p-2 text-gray-400 hover:text-blue-600">
                    <RefreshCw className={"w-4 h-4 " + (loading.sync[b.account_id] ? 'animate-spin' : '')} />
                  </button>
                </div>
                <div className="text-4xl font-bold text-gray-900">{formatPoints(b.current_balance)}</div>
              </div>
            ))}
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-12">
          <section>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Best Use Recommendations</h2>
            <div className="bg-white rounded-2xl p-8 shadow-sm">
              {recommendations.map((rec:any) => (
                <div key={rec.id} className="mb-6 last:mb-0">
                  <h3 className="text-2xl font-bold text-gray-900 mb-4 leading-tight">{rec.title}</h3>
                  <p className="text-gray-600 mb-6 text-base leading-relaxed">{rec.description}</p>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-4 rounded-xl transition-colors text-lg">Book Now</button>
                </div>
              ))}
            </div>
          </section>

          <section className="flex items-center justify-center">
            <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl p-8 w-full h-80 flex items-center justify-center relative overflow-hidden">
              <div className="absolute top-8 right-8 transform rotate-12">
                <Plane className="w-16 h-16 text-blue-800" />
              </div>
              <div className="absolute bottom-0 left-0 right-0 flex justify-center items-end space-x-1">
                <div className="w-8 h-16 bg-gradient-to-t from-blue-400 to-blue-300 rounded-t"></div>
                <div className="w-6 h-12 bg-gradient-to-t from-blue-500 to-blue-400 rounded-t"></div>
                <div className="w-10 h-20 bg-gradient-to-t from-blue-600 to-blue-500 rounded-t"></div>
                <div className="w-12 h-24 bg-gradient-to-t from-blue-700 to-blue-600 rounded-t"></div>
                <div className="w-14 h-28 bg-gradient-to-t from-blue-800 to-blue-700 rounded-t"></div>
              </div>
            </div>
          </section>
        </div>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Search</h2>
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <div className="flex space-x-4">
              <div className="flex-1">
                <input value={searchQuery} onChange={(e)=>setSearchQuery(e.target.value)} placeholder="I want to go to Paris in June for 7 days" className="w-full px-6 py-4 text-lg border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500" onKeyPress={(e)=> e.key === 'Enter' && handleSearch()} />
              </div>
              <button onClick={handleSearch} className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-8 py-4 rounded-xl font-semibold transition-colors flex items-center space-x-2">
                <Search className="w-5 h-5" /><span>Search</span>
              </button>
            </div>
          </div>
        </section>

        {searchResults && (
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Search Results</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {searchResults.recommendations?.map((rec:any) => (
                <div key={rec.id} className="bg-white rounded-2xl p-6 shadow-md border hover:shadow-lg transition-all">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-bold text-gray-900">{rec.title}</h3>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-green-600">${rec.estimated_value?.toLocaleString()}</div>
                      <div className="text-sm text-gray-500">est. value</div>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-4">{rec.description}</p>
                  <div className="bg-gray-50 rounded-lg p-4 mb-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className="text-gray-500 text-sm">Points Required:</span>
                        <div className="font-bold text-blue-600">{formatPoints(rec.points_required)}</div>
                      </div>
                      <div>
                        <span className="text-gray-500 text-sm">Program:</span>
                        <div className="font-bold text-gray-900 uppercase">{rec.program_name}</div>
                      </div>
                    </div>
                  </div>
                  <button className="w-full bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-bold px-6 py-3 rounded-xl transition-all">Book This Trip</button>
                </div>
              ))}
            </div>
            {searchResults.total_value && (
              <div className="mt-8 text-center">
                <div className="inline-flex items-center space-x-2 bg-green-100 text-green-800 px-6 py-3 rounded-full">
                  <DollarSign className="w-5 h-5" />
                  <span className="font-bold text-lg">Total Trip Value: ${searchResults.total_value?.toLocaleString()}</span>
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
