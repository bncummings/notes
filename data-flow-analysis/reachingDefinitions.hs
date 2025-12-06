{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Use newtype instead of data" #-}
module ReachingDefinitions where
import Data.List ( (\\), nub )
import Data.Map (union)

data Expr =
         Var String
         | Const String
         | BinOp Expr Expr
         deriving (Show, Eq)

data TAC =
         Assign DefId Expr     -- x = y
         deriving (Show, Eq)

type CFG = [Node]
data Node = Node
    { nodeId :: NodeId
    , nodeDefs :: DefSet
    , nodeUses :: UseSet
    , nodeSuccs :: SuccSet
    , nodePreds :: PredSet
    } deriving (Show, Eq)

type NodeId = String
type DefId = String
type Instr = TAC
type DefSet = [DefId]
type UseSet = [DefId]
type PredSet = [NodeId]
type SuccSet = [NodeId]
type RDs = ( [ (NodeId,[NodeId]) ], [ (NodeId,[NodeId]) ] )

nodeGen :: Node -> [NodeId]
nodeGen node
    | null (nodeDefs node) = [] -- if there are no defs, then there are no gen
    | otherwise = [nodeId node]

nodeKill :: CFG -> Node -> [NodeId]
nodeKill cfg node = nodeDefSet cfg node \\ [nodeId node]

-- the set of nodes where a variabl 't' is defined
nodeDefSet :: CFG -> Node -> [NodeId]
nodeDefSet cfg node =
    case nodeDefs node of
        [t] -> [id | Node id, i, ds, us, scs, t `elem` ds, prds <- cfg]
        [] -> []
        otherwise -> error "nodeDefSet: multiple defs"

--helper funcions
untilConverges (a:b:rest) | a == b = a
untilConverges (a:b:rest) = untilConverges (b:rest)
zip2 (rdsin,rdsout) = zip rdsin rdsout
bigU sets = nub (concat sets)


reachingDefinitionsOf :: CFG -> RDs
reachingDefinitionsOf cfg = untilConverges (iterate updateRDs initialRDs)
 where
 initialRDs :: RDs
 initialRDs = ( [(nodeId n,[]) | n <- cfg], [(nodeId n,[]) | n <- cfg] )

 updateRDs :: RDs -> RDs
 updateRDs rds = unzip (map (updateRD rds) (zip2 rds))
 updateRD (rdins_sofar, rdouts_sofar) ((id,rdins), (sameid,rdouts)) =
    ((id,rdins'), (id,rdouts'))
         where
            rdins' = bigU [retrieve s rdouts_sofar | s <- nodePreds node]
            rdouts' = nodeGen node `union` (rdInsOf node \\ nodeKill cfg node )
                where
                    rdInsOf node = retrieve (nodeId node) rdins_sofar
                    node = idToNode cfg id
