import { useSession } from '@/hooks/SessionContext';
import { useUser, useTasteProfile } from '@/services/queries';
import { TasteRadarChart } from '@/components/TasteRadarChart';
import { getQualitativeLabel } from '@/components/TasteDimensionCard';
import { TasteProfileSkeleton } from '@/components/TasteProfileSkeleton';
import { ErrorState } from '@/components/ErrorState';
import { ArrowLeft, Dna, Sparkles, ShieldCheck, History, Info, RefreshCw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export function TasteDNADashboard() {
  const { userId } = useSession();
  const navigate = useNavigate();

  const { data: user, isLoading: isUserLoading, isError: isUserError } = useUser(userId);
  const { data: profile, isLoading: isProfileLoading, isError: isProfileError, refetch } = useTasteProfile(userId);

  if (isUserLoading || isProfileLoading) {
    return <TasteProfileSkeleton />;
  }

  if (isUserError || isProfileError || !user || !profile) {
    return <ErrorState message="Failed to load your Taste DNA continuous learning profile." onRetry={() => navigate('/quiz')} />;
  }

  const dnaMatrix = profile.dna_matrix;

  const dimensionsList = [
    { key: 'spice', label: 'Spice', val: profile.spice_preference, detail: dnaMatrix?.spice },
    { key: 'saltiness', label: 'Saltiness', val: profile.saltiness_preference, detail: dnaMatrix?.saltiness },
    { key: 'sweetness', label: 'Sweetness', val: profile.sweetness_preference, detail: dnaMatrix?.sweetness },
    { key: 'tanginess', label: 'Tanginess', val: profile.tanginess_preference, detail: dnaMatrix?.tanginess },
    { key: 'creaminess', label: 'Creaminess', val: profile.creaminess_preference, detail: dnaMatrix?.creaminess },
    { key: 'oiliness', label: 'Oiliness', val: profile.oiliness_preference, detail: dnaMatrix?.oiliness },
    { key: 'masala_intensity', label: 'Masala Intensity', val: profile.masala_intensity_preference, detail: dnaMatrix?.masala_intensity },
    { key: 'crunchiness', label: 'Crunch', val: profile.crunchiness_preference, detail: dnaMatrix?.crunchiness },
  ];

  const radarData = dimensionsList.map(d => ({
    label: d.label,
    value: d.val
  }));

  const overallConfidencePct = Math.round((profile.confidence_score || 0.55) * 100);
  const evolutionEvents = dnaMatrix?.recent_evolution || [
    {
      date: new Date().toISOString().split('T')[0],
      event: 'Taste DNA Baseline Initialized',
      description: 'Initial Taste DNA calculated from onboarding quiz responses.',
      source: 'Onboarding Quiz'
    }
  ];

  return (
    <div className="flex flex-col min-h-screen bg-background pb-16">
      {/* Header Bar */}
      <header className="sticky top-0 z-30 flex items-center justify-between p-4 bg-background/80 backdrop-blur border-b border-border">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/restaurant')}
            className="p-2 rounded-full hover:bg-muted transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-primary/10 text-primary rounded-xl">
              <Dna className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-extrabold tracking-tight">My Taste DNA</h1>
              <p className="text-xs text-muted-foreground">Continuous Learning Intelligence Engine</p>
            </div>
          </div>
        </div>

        <button
          onClick={() => refetch()}
          className="flex items-center gap-1.5 text-xs font-bold text-muted-foreground hover:text-foreground px-3 py-1.5 rounded-lg border border-border bg-card"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </header>

      <main className="flex-1 max-w-6xl mx-auto w-full p-4 md:p-8 space-y-8">
        {/* Portability Alert Banner */}
        <div className="bg-primary/5 border border-primary/20 rounded-2xl p-4 md:p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2.5 bg-primary/10 text-primary rounded-xl mt-0.5">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-base font-bold text-foreground flex items-center gap-2">
                <span>Taste DNA Portability</span>
                <span className="text-[10px] uppercase font-extrabold px-2 py-0.5 bg-primary text-primary-foreground rounded-full">Active IP</span>
              </h2>
              <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                Your Taste DNA belongs strictly to you. It evolves with every meal and seamlessly travels across all TasteAI-partnered restaurants.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/quiz')}
            className="text-xs font-bold text-primary hover:underline self-end md:self-center whitespace-nowrap"
          >
            Retake Baseline Quiz →
          </button>
        </div>

        {/* Top KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-card border border-border p-5 rounded-2xl flex flex-col justify-between">
            <span className="text-xs font-bold uppercase text-muted-foreground tracking-wider">Overall Completion</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-black text-foreground">100%</span>
              <span className="text-xs font-medium text-emerald-500">Fully Mapped</span>
            </div>
            <p className="text-[11px] text-muted-foreground mt-2">All 8 permanent flavor dimensions initialized</p>
          </div>

          <div className="bg-card border border-border p-5 rounded-2xl flex flex-col justify-between">
            <span className="text-xs font-bold uppercase text-muted-foreground tracking-wider">Learning Confidence</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-black text-primary">{overallConfidencePct}%</span>
              <span className="text-xs font-bold px-2 py-0.5 bg-primary/10 text-primary rounded-full">
                {overallConfidencePct > 75 ? 'High Precision' : overallConfidencePct > 55 ? 'Learning' : 'Initial'}
              </span>
            </div>
            <p className="text-[11px] text-muted-foreground mt-2">Increases monotonically with meal feedback</p>
          </div>

          <div className="bg-card border border-border p-5 rounded-2xl flex flex-col justify-between">
            <span className="text-xs font-bold uppercase text-muted-foreground tracking-wider">Primary Intelligence Pillar</span>
            <div className="flex items-center gap-2 mt-2">
              <Sparkles className="w-5 h-5 text-amber-500" />
              <span className="text-lg font-bold text-foreground">Taste DNA Engine</span>
            </div>
            <p className="text-[11px] text-muted-foreground mt-2">Continuous gradual learning (lerp smoothing)</p>
          </div>
        </div>

        {/* Main Grid: Radar Chart + Dimensions */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Radar Chart Column */}
          <div className="lg:col-span-5 space-y-6">
            <TasteRadarChart dimensions={radarData} />

            {/* Learning Sources Breakdown Box */}
            <div className="bg-card border border-border p-5 rounded-2xl space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-muted-foreground">
                <Info className="w-4 h-4 text-primary" />
                <span>Learning Sources Weights</span>
              </div>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Onboarding Quiz</span>
                  <span className="font-semibold">Baseline (35%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Post-Meal Feedback</span>
                  <span className="font-semibold">Medium Weight (25%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Repeated Positive Orders</span>
                  <span className="font-semibold">Medium Weight (25%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Repeated Reorders</span>
                  <span className="font-semibold text-primary">High Weight (40%)</span>
                </div>
              </div>
            </div>
          </div>

          {/* 8 Dimension Cards Column */}
          <div className="lg:col-span-7 space-y-4">
            <h3 className="text-base font-bold text-foreground">Eight Permanent Dimensions</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {dimensionsList.map((dim) => {
                const percentage = Math.round(dim.val * 100);
                const qualitative = getQualitativeLabel(dim.key, dim.val);
                const confPct = Math.round((dim.detail?.confidence || profile.confidence_score || 0.55) * 100);
                const sources = dim.detail?.sources || ['Quiz Baseline'];

                return (
                  <div key={dim.key} className="bg-card border border-border p-4 rounded-2xl flex flex-col justify-between gap-3 hover:border-primary/50 transition-colors">
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm font-bold text-foreground">{dim.label}</span>
                        <span className="text-[10px] font-bold px-2 py-0.5 bg-primary/10 text-primary rounded-full">
                          {confPct}% Conf.
                        </span>
                      </div>
                      <div className="flex items-baseline justify-between text-xs mt-1">
                        <span className="font-extrabold text-primary">{qualitative}</span>
                        <span className="text-muted-foreground font-medium">{percentage}%</span>
                      </div>
                    </div>

                    <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-primary transition-all duration-700 ease-out rounded-full" 
                        style={{ width: `${percentage}%` }}
                      />
                    </div>

                    <div className="text-[10px] text-muted-foreground flex justify-between items-center pt-1 border-t border-border/50">
                      <span>Learned from:</span>
                      <span className="font-semibold truncate max-w-[140px] text-right">{sources.join(', ')}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Learning Evolution Timeline */}
        <div className="bg-card border border-border p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="w-5 h-5 text-primary" />
              <h3 className="text-base font-bold text-foreground">Taste DNA Evolution Timeline</h3>
            </div>
            <span className="text-xs text-muted-foreground">Incremental Learning Events</span>
          </div>

          <div className="space-y-3 pt-2">
            {evolutionEvents.map((evt: any, idx: number) => (
              <div key={idx} className="flex items-start gap-4 p-3 bg-muted/30 rounded-xl border border-border/40">
                <div className="w-2 h-2 rounded-full bg-primary mt-2 flex-shrink-0" />
                <div className="flex-1">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold text-foreground">{evt.event}</span>
                    <span className="text-[10px] text-muted-foreground">{evt.date}</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-0.5">{evt.description}</p>
                </div>
                <span className="text-[10px] font-semibold px-2 py-0.5 bg-background border border-border rounded-lg text-muted-foreground whitespace-nowrap">
                  {evt.source}
                </span>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
