import copy

def createBins( binning, cut ):

    if isinstance(binning[0], dict):
        return _createBins( binning, cut )

    else:
        binDefinition = {'vars' : [], 'bins' : []}

        for i, b in enumerate(binning):
            bins = _createBins( b, cut )
            binDefinition['vars'] += bins['vars']
            binDefinition['bins'] += bins['bins']

        binDefinition['vars'] = set(binDefinition['vars'])
        for i, b in enumerate(binDefinition["bins"]):
            b["name"] = 'bin{:02d}'.format(i) + b["name"][5:]

        return binDefinition

def _createBins( binning, cut ):
    binCut = None
    nbin = 0

    nbin = 1

    nvars = len(binning)
    listOfIndex = [[-1] * nvars]

    ### first map nD bins in a single list
    for iv, b in enumerate(binning):
        var = b['var']
        if not b.has_key('type') or not b.has_key('bins'):
            print 'binning is not complete for var %s' % var
            return listOfIndex
        # For an int variable, there are as many bins as values, while for a
        # float variable there is a bin for every interval between values
        nb1D = len(b['bins']) - (b['type'] == 'float')
        nbin = nbin * nb1D

        listOfIndexInit = copy.deepcopy(listOfIndex)
        for ib_v in range(nb1D):
            if ib_v == 0 :
                for ib in range(len(listOfIndex)):
                    listOfIndex[ib][iv] = ib_v
            else:
                for ib in range(len(listOfIndexInit)):
                    listOfIndexInit[ib][iv] = ib_v

                listOfIndex.extend(copy.deepcopy(listOfIndexInit))

    listOfBins = []
    nbins = len(listOfIndex)
    for ibin, ix in enumerate(listOfIndex):
        ### make bin definition
        binCut   = None
        binName  = 'bin%02d'%ibin
        if nbins > 100   :  binName  = 'bin%03d'%ibin
        if nbins > 1000  :  binName  = 'bin%04d'%ibin
        if nbins > 10000 :  binName  = 'bin%d'%ibin

        binTitle = ''
        binVars = {}
        if not cut is None:
            binCut = cut

        for iv in range(len(ix)):
            var     = binning[iv]['var']
            bins1D  = binning[iv]['bins']
            varType = binning[iv]['type']
            if varType == 'float' :
                if binCut is None:
                    binCut   = '%s >= %f && %s < %f' % (var,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                    binTitle = '%1.3f < %s < %1.3f'  % (bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                else:
                    binCut   = '%s && %s >= %f && %s < %f' % (binCut  ,var,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                    binTitle = '%s; %1.3f < %s < %1.3f'    % (binTitle,bins1D[ix[iv]],var,bins1D[ix[iv]+1])
                binName  = '%s_%s_%1.2fTo%1.2f'  % (binName ,var,bins1D[ix[iv]],bins1D[ix[iv]+1])
                binVars[var] = { 'min': bins1D[ix[iv]], 'max': bins1D[ix[iv]+1]}


            if varType == 'int' :
                if binCut is None:
                    binCut   = '%s == %d' % (var,bins1D[ix[iv]])
                    binTitle = '%s = %d'  % (var,bins1D[ix[iv]])
                else:
                    binCut   = '%s && %s == %d' % (binCut,var,bins1D[ix[iv]])
                    binTitle = '%s; %s = %d'    % (binTitle,var,bins1D[ix[iv]])
                binName  = '%s_%sEq%d' % (binName ,var,bins1D[ix[iv]])
                binVars[var] = { 'min': bins1D[ix[iv]], 'max': bins1D[ix[iv]]}

            binName = binName.replace('-','m').replace('.','p')

        listOfBins.append({'cut' : binCut, 'title': binTitle, 'name' : binName, 'vars' : binVars })

    listOfVars = []
    for iv in  range(len(binning)):
        listOfVars.append(binning[iv]['var'])

    binDefinition = {
        'vars' : listOfVars,
        'bins' : listOfBins
        }
    return binDefinition

def tuneCuts( bindef, cuts ) :
    if cuts is None:
        return

    for ibin in cuts.keys():
        cut0 = bindef['bins'][ibin]['cut']
        cut1 = cuts[ibin]
        bindef['bins'][ibin]['cut'] = '%s && %s ' % (cut0,cut1)
