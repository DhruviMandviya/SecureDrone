import { useState, useEffect, useRef } from 'react';

/**
 * Custom hook to poll a given async function at a specific interval.
 * Returns the latest data, loading state, error, and a manual refresh function.
 */
export function usePolling<T>(
  fetchFn: () => Promise<T>,
  intervalMs: number,
  immediate: boolean = true
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const savedFetchFn = useRef(fetchFn);

  useEffect(() => {
    savedFetchFn.current = fetchFn;
  }, [fetchFn]);

  useEffect(() => {
    let timeoutId: number;
    let isMounted = true;

    const executePoll = async () => {
      try {
        if (!data) setLoading(true);
        const result = await savedFetchFn.current();
        if (isMounted) {
          setData(result);
          setError(null);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
          timeoutId = window.setTimeout(executePoll, intervalMs);
        }
      }
    };

    if (immediate) {
      executePoll();
    } else {
      timeoutId = window.setTimeout(executePoll, intervalMs);
    }

    return () => {
      isMounted = false;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [intervalMs, immediate]);

  // Provide manual refresh capability
  const refresh = async () => {
    try {
      setLoading(true);
      const result = await savedFetchFn.current();
      setData(result);
      setError(null);
    } catch (err: any) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refresh };
}
